from typing import Any

from sqlalchemy.orm import Session

from app.core.db_utils import save_and_refresh
from app.core.pagination import apply_pagination, get_pagination_metadata
from app.models.attendee import EventRegistration
from app.models.event import Event


def register_to_event(db: Session, user_id: int, event_id: int) -> EventRegistration:
    """
    Registra un usuario a un evento.

    Nota: Las validaciones (evento existe, capacidad, duplicados)
    se hacen en el servicio, no aquí.
    """
    registration = EventRegistration(user_id=user_id, event_id=event_id)
    return save_and_refresh(db, registration)


def unregister_from_event(db: Session, user_id: int, event_id: int) -> bool:
    """Cancela el registro de un usuario a un evento (soft delete)"""
    from app.core.db_utils import soft_delete

    registration = (
        db.query(EventRegistration)
        .filter(
            EventRegistration.user_id == user_id,
            EventRegistration.event_id == event_id,
            EventRegistration.deleted_at.is_(None),
            EventRegistration.is_deleted.is_(False),
        )
        .first()
    )

    if not registration:
        return False

    soft_delete(db, registration)
    return True


def soft_delete_registration(db: Session, registration_id: int) -> bool:
    """Realiza soft delete de un registro"""
    from app.core.db_utils import soft_delete

    registration = (
        db.query(EventRegistration)
        .filter(
            EventRegistration.id == registration_id,
            EventRegistration.deleted_at.is_(None),
            EventRegistration.is_deleted.is_(False),
        )
        .first()
    )

    if not registration:
        return False

    soft_delete(db, registration)
    return True


def get_user_registrations(db: Session, user_id: int) -> list[EventRegistration]:
    """Obtiene todos los registros de un usuario (excluye eliminados)"""
    return (
        db.query(EventRegistration)
        .filter(
            EventRegistration.user_id == user_id,
            EventRegistration.deleted_at.is_(None),
            EventRegistration.is_deleted.is_(False),
        )
        .all()
    )


def _get_user_registered_events_query(db: Session, user_id: int):
    """
    Query base para obtener eventos registrados por un usuario.
    Retorna la query sin paginación para reutilizar.
    """
    return (
        db.query(Event)
        .join(EventRegistration, Event.id == EventRegistration.event_id)
        .filter(
            EventRegistration.user_id == user_id,
            EventRegistration.deleted_at.is_(None),
            EventRegistration.is_deleted.is_(False),
            Event.deleted_at.is_(None),
            Event.is_deleted.is_(False),
        )
        .order_by(Event.created_at.desc())
    )


def get_user_registered_events(
    db: Session, user_id: int, page: int = 1, per_page: int = 20
) -> tuple[list[Event], dict[str, Any]]:
    """
    Obtiene los eventos a los que un usuario está registrado (excluye eliminados) con paginación.

    Returns:
        Tuple[List[Event], Dict[str, Any]]: Lista de eventos y metadata de paginación
    """
    query = _get_user_registered_events_query(db, user_id)
    pagination_metadata = get_pagination_metadata(query, page=page, per_page=per_page)
    paginated_query = apply_pagination(query, page=page, per_page=per_page)
    events = paginated_query.all()

    return events, pagination_metadata


def get_user_registered_events_all(db: Session, user_id: int) -> list[Event]:
    """
    Obtiene todos los eventos a los que un usuario está registrado (sin paginación).
    Útil para casos como el perfil del usuario donde se necesitan todos los eventos.

    Returns:
        List[Event]: Lista completa de eventos registrados
    """
    query = _get_user_registered_events_query(db, user_id)
    return query.all()


def get_event_registrations(db: Session, event_id: int) -> list[EventRegistration]:
    """Obtiene todos los registros de un evento (excluye eliminados)"""
    return (
        db.query(EventRegistration)
        .filter(
            EventRegistration.event_id == event_id,
            EventRegistration.deleted_at.is_(None),
            EventRegistration.is_deleted.is_(False),
        )
        .all()
    )


def is_user_registered(db: Session, user_id: int, event_id: int) -> bool:
    """Verifica si un usuario está registrado en un evento (excluye eliminados)"""
    return (
        db.query(EventRegistration)
        .filter(
            EventRegistration.user_id == user_id,
            EventRegistration.event_id == event_id,
            EventRegistration.deleted_at.is_(None),
            EventRegistration.is_deleted.is_(False),
        )
        .first()
        is not None
    )
