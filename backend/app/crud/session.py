from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.core.db_utils import save_and_refresh, update_and_refresh
from app.core.pagination import apply_pagination, get_pagination_metadata
from app.models.session import Session as EventSession
from app.schemas.session import SessionCreate, SessionUpdate


def get_session(db: Session, session_id: int) -> EventSession | None:
    """Obtiene una sesión por ID (excluye eliminadas)"""
    return (
        db.query(EventSession)
        .filter(
            EventSession.id == session_id,
            EventSession.deleted_at.is_(None),
            EventSession.is_deleted.is_(False),
        )
        .first()
    )


def get_event_sessions(
    db: Session, event_id: int, page: int = 1, per_page: int = 20
) -> tuple[list[EventSession], dict[str, Any]]:
    """
    Obtiene las sesiones de un evento (excluye eliminadas) con paginación.

    Returns:
        Tuple[List[EventSession], Dict[str, Any]]: Lista de sesiones y metadata de paginación
    """
    query = (
        db.query(EventSession)
        .filter(
            EventSession.event_id == event_id,
            EventSession.deleted_at.is_(None),
            EventSession.is_deleted.is_(False),
        )
        .order_by(EventSession.start_time.asc())
    )
    pagination_metadata = get_pagination_metadata(query, page=page, per_page=per_page)
    paginated_query = apply_pagination(query, page=page, per_page=per_page)
    sessions = paginated_query.all()

    return sessions, pagination_metadata


def create_session(db: Session, session: SessionCreate) -> EventSession:
    """Crea una nueva sesión"""
    db_session = EventSession(**session.model_dump())
    return save_and_refresh(db, db_session)


def update_session(
    db: Session, session_id: int, session_update: SessionUpdate
) -> EventSession | None:
    """Actualiza una sesión"""
    db_session = get_session(db, session_id)
    if not db_session:
        return None

    update_data = session_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_session, field, value)
    db_session.updated_at = datetime.utcnow()

    return update_and_refresh(db, db_session)


def soft_delete_session(db: Session, session_id: int) -> bool:
    """Realiza soft delete de una sesión"""
    from app.core.db_utils import soft_delete

    db_session = get_session(db, session_id)
    if not db_session:
        return False

    soft_delete(db, db_session)
    return True
