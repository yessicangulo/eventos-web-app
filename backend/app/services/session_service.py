"""
Servicio de sesiones - Lógica de negocio para gestión de sesiones de eventos
"""

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ValidationError
from app.crud import session as crud_session
from app.models.event import Event
from app.models.session import Session as EventSession
from app.models.user import User
from app.schemas.session import SessionCreate, SessionUpdate
from app.services.event_service import EventService


def _validate_session_within_event_range(
    start_time: datetime, end_time: datetime, event: Event
) -> None:
    """
    Valida que los horarios de la sesión estén dentro del rango del evento.

    Args:
        start_time: Fecha/hora de inicio de la sesión
        end_time: Fecha/hora de fin de la sesión
        event: Evento al que pertenece la sesión

    Raises:
        ValidationError: Si la sesión no está dentro del rango del evento
    """
    if start_time < event.start_date or end_time > event.end_date:
        raise ValidationError("La sesión debe estar dentro del rango de fechas del evento")


def _validate_session_capacity(session_capacity: int | None, event: Event) -> None:
    """
    Valida que la capacidad de la sesión sea menor o igual a la capacidad del evento.

    Args:
        session_capacity: Capacidad de la sesión (puede ser None)
        event: Evento al que pertenece la sesión

    Raises:
        ValidationError: Si la capacidad de la sesión excede la capacidad del evento
    """
    if session_capacity is not None and session_capacity > event.capacity:
        raise ValidationError(
            f"La capacidad de la sesión ({session_capacity}) no puede ser mayor "
            f"que la capacidad del evento ({event.capacity})"
        )


class SessionService:
    """Servicio para operaciones relacionadas con sesiones"""

    @staticmethod
    def get_session(db: Session, session_id: int) -> EventSession:
        """
        Obtiene una sesión por ID

        Raises:
            NotFoundError: Si la sesión no existe
        """
        session = crud_session.get_session(db, session_id=session_id)
        if not session:
            raise NotFoundError("Sesión no encontrada")
        return session

    @staticmethod
    def get_event_sessions(
        db: Session, event_id: int, page: int = 1, per_page: int = 20
    ) -> tuple[list[EventSession], dict[str, Any]]:
        """
        Obtiene las sesiones de un evento con paginación

        Raises:
            NotFoundError: Si el evento no existe

        Returns:
            Tuple[List[EventSession], Dict[str, Any]]: Lista de sesiones y metadata de paginación
        """
        EventService.get_event(db, event_id)
        return crud_session.get_event_sessions(db, event_id=event_id, page=page, per_page=per_page)

    @staticmethod
    def create_session(db: Session, session_data: SessionCreate, user: User) -> EventSession:
        """
        Crea una nueva sesión

        Raises:
            NotFoundError: Si el evento no existe
            ValidationError: Si hay errores de validación
        """
        event = EventService.verify_event_exists(db, session_data.event_id)
        _validate_session_within_event_range(session_data.start_time, session_data.end_time, event)
        _validate_session_capacity(session_data.capacity, event)

        return crud_session.create_session(db=db, session=session_data)

    @staticmethod
    def update_session(
        db: Session,
        session_id: int,
        session_update: SessionUpdate,
    ) -> EventSession:
        """
        Actualiza una sesión

        Raises:
            NotFoundError: Si la sesión no existe
            ValidationError: Si la sesión no está dentro del rango del evento
        """
        db_session = SessionService.get_session(db, session_id)
        event = EventService.verify_event_exists(db, db_session.event_id)
        if session_update.start_time or session_update.end_time:
            start_time = session_update.start_time or db_session.start_time
            end_time = session_update.end_time or db_session.end_time

            _validate_session_within_event_range(start_time, end_time, event)
        if session_update.capacity:
            _validate_session_capacity(session_update.capacity, event)

        updated_session = crud_session.update_session(
            db, session_id=session_id, session_update=session_update
        )

        if not updated_session:
            raise ValidationError("Error al actualizar la sesión")

        return updated_session

    @staticmethod
    def delete_session(db: Session, session_id: int) -> None:
        """
        Realiza soft delete de una sesión

        Raises:
            NotFoundError: Si la sesión no existe
        """
        SessionService.get_session(db, session_id)

        success = crud_session.soft_delete_session(db, session_id=session_id)
        if not success:
            raise ValidationError("Error al eliminar la sesión")
