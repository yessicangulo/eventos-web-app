import unicodedata
from datetime import datetime
from typing import Any

from sqlalchemy import func, update
from sqlalchemy.orm import Session, joinedload

from app.core.db_utils import save_and_refresh, update_and_refresh
from app.core.pagination import apply_pagination, get_pagination_metadata
from app.models.event import Event, EventStatus, EventStatusDB
from app.schemas.event import EventCreate, EventUpdate


def _normalize_text(text: str) -> str:
    """
    Normaliza un texto removiendo acentos y convirtiendo a minúsculas.
    Útil para búsquedas que ignoran acentos.

    Ejemplo:
        "Tecnología" -> "tecnologia"
        "José" -> "jose"
    """
    # Normalizar a NFD (decomponer caracteres acentuados)
    nfd = unicodedata.normalize("NFD", text.lower())
    # Filtrar solo caracteres que no sean marcas diacríticas
    return "".join(char for char in nfd if unicodedata.category(char) != "Mn")


def _build_computed_status_filter(status: EventStatus):
    """
    Construye un filtro SQL para computed_status.

    La lógica es:
    - Si status en BD es CANCELLED: retornar ese estado
    - Si status en BD es SCHEDULED: calcular basado en fechas:
      * Si now > end_date → COMPLETED
      * Si start_date <= now <= end_date → ONGOING
      * Si now < start_date → SCHEDULED
    """
    now = datetime.utcnow()

    # Para estados manuales, filtrar directamente por la columna
    if status == EventStatus.CANCELLED:
        return Event.status == EventStatusDB.CANCELLED

    # Filtrar por el estado computado
    if status == EventStatus.SCHEDULED:
        return (Event.status == EventStatusDB.SCHEDULED) & (now < Event.start_date)
    elif status == EventStatus.ONGOING:
        return (
            (Event.status == EventStatusDB.SCHEDULED)
            & (Event.start_date <= now)
            & (now <= Event.end_date)
        )
    elif status == EventStatus.COMPLETED:
        return (Event.status == EventStatusDB.SCHEDULED) & (Event.end_date < now)

    return None


def get_event(db: Session, event_id: int, include_sessions: bool = False) -> Event | None:
    """
    Obtiene un evento por ID (excluye eliminados con soft delete)

    Args:
        db: Sesión de base de datos
        event_id: ID del evento
        include_sessions: Si True, carga las sesiones en la misma query (eager loading)

    Returns:
        Event o None si no existe o está eliminado
    """
    query = db.query(Event).filter(
        Event.id == event_id, Event.deleted_at.is_(None), Event.is_deleted.is_(False)
    )
    if include_sessions:
        query = query.options(joinedload(Event.sessions))

    return query.first()


def get_events(
    db: Session,
    page: int = 1,
    per_page: int = 20,
    search: str | None = None,
    status: EventStatus | None = None,
) -> tuple[list[Event], dict[str, Any]]:
    """
    Lista eventos con filtros opcionales y paginación.

    Returns:
        Tuple[List[Event], Dict]: (eventos, metadata de paginación)
    """
    query = db.query(Event).filter(Event.deleted_at.is_(None), Event.is_deleted.is_(False))
    if search:
        # Normalizar el término de búsqueda: convertir a minúsculas y remover acentos
        normalized_search = _normalize_text(search)

        # Usar unaccent de PostgreSQL para normalizar acentos en el campo name
        # Requiere: CREATE EXTENSION IF NOT EXISTS unaccent;
        query = query.filter(func.unaccent(func.lower(Event.name)).ilike(f"%{normalized_search}%"))
    if status:
        status_filter = _build_computed_status_filter(status)
        if status_filter is not None:
            query = query.filter(status_filter)
    pagination_metadata = get_pagination_metadata(query, page=page, per_page=per_page)
    query = apply_pagination(query, page=page, per_page=per_page)

    events = query.all()

    return events, pagination_metadata


def create_event(db: Session, event: EventCreate, creator_id: int) -> Event:
    """Crea un nuevo evento"""
    db_event = Event(**event.model_dump(), creator_id=creator_id)
    return save_and_refresh(db, db_event)


def update_event(db: Session, event_id: int, event_update: EventUpdate) -> Event | None:
    """Actualiza un evento"""
    db_event = get_event(db, event_id)
    if not db_event:
        return None

    update_data = event_update.model_dump(exclude_unset=True)

    # Convertir EventStatus a EventStatusDB si se está actualizando el status
    if "status" in update_data:
        status_value = update_data["status"]
        if isinstance(status_value, EventStatus):
            update_data["status"] = EventStatusDB(status_value.value)
        elif isinstance(status_value, str):
            try:
                update_data["status"] = EventStatusDB(status_value)
            except ValueError:
                try:
                    event_status = EventStatus(status_value)
                    update_data["status"] = EventStatusDB(event_status.value)
                except ValueError:
                    pass  # Dejar que SQLAlchemy valide

    for field, value in update_data.items():
        setattr(db_event, field, value)

    db_event.updated_at = datetime.utcnow()
    return update_and_refresh(db, db_event)


def soft_delete_event(db: Session, event_id: int) -> bool:
    """
    Realiza soft delete de un evento y sus relaciones (cascada) usando bulk updates

    Args:
        db: Sesión de base de datos
        event_id: ID del evento a eliminar

    Returns:
        True si se eliminó correctamente, False si no existe
    """
    from app.models.attendee import EventRegistration
    from app.models.session import Session

    db_event = get_event(db, event_id)
    if not db_event:
        return False

    now = datetime.utcnow()

    # Bulk soft delete de entidades relacionadas (cascada)
    db.execute(
        update(Session)
        .where(
            Session.event_id == event_id,
            Session.deleted_at.is_(None),
            Session.is_deleted.is_(False),
        )
        .values(deleted_at=now, is_deleted=True, updated_at=now)
    )

    db.execute(
        update(EventRegistration)
        .where(
            EventRegistration.event_id == event_id,
            EventRegistration.deleted_at.is_(None),
            EventRegistration.is_deleted.is_(False),
        )
        .values(deleted_at=now, is_deleted=True)
    )

    # Soft delete del evento
    db.execute(
        update(Event)
        .where(Event.id == event_id)
        .values(deleted_at=now, is_deleted=True, updated_at=now)
    )

    db.commit()
    return True


def _get_user_events_query(db: Session, user_id: int):
    """
    Query base para obtener eventos creados por un usuario.
    Retorna la query sin paginación para reutilizar.
    """
    return (
        db.query(Event)
        .filter(
            Event.creator_id == user_id, Event.deleted_at.is_(None), Event.is_deleted.is_(False)
        )
        .order_by(Event.created_at.desc())
    )


def get_user_events(
    db: Session, user_id: int, page: int = 1, per_page: int = 20
) -> tuple[list[Event], dict[str, Any]]:
    """
    Obtiene eventos creados por un usuario (excluye eliminados) con paginación.

    Returns:
        Tuple[List[Event], Dict[str, Any]]: Lista de eventos y metadata de paginación
    """
    query = _get_user_events_query(db, user_id)

    pagination_metadata = get_pagination_metadata(query, page=page, per_page=per_page)

    paginated_query = apply_pagination(query, page=page, per_page=per_page)
    events = paginated_query.all()

    return events, pagination_metadata


def get_user_events_all(db: Session, user_id: int) -> list[Event]:
    """
    Obtiene todos los eventos creados por un usuario (sin paginación).
    Útil para casos como el perfil del usuario donde se necesitan todos los eventos.

    Returns:
        List[Event]: Lista completa de eventos creados
    """
    query = _get_user_events_query(db, user_id)
    return query.all()
