"""
Servicio de eventos - Lógica de negocio para gestión de eventos
"""

from typing import Any

from sqlalchemy.orm import Session

from app.core.event_validations import validate_event_update
from app.core.exceptions import NotFoundError, ValidationError
from app.crud import event as crud_event
from app.models.event import Event, EventStatus, EventStatusDB
from app.models.user import User
from app.schemas.event import EventCreate, EventUpdate


class EventService:
    """Servicio para operaciones relacionadas con eventos"""

    @staticmethod
    def get_event(db: Session, event_id: int, include_sessions: bool = False) -> Event:
        """
        Obtiene un evento por ID

        Args:
            db: Sesión de base de datos
            event_id: ID del evento
            include_sessions: Si True, carga las sesiones en la misma query (eager loading)

        Raises:
            NotFoundError: Si el evento no existe

        Returns:
            Event con sesiones cargadas si include_sessions=True
        """
        event = crud_event.get_event(db, event_id=event_id, include_sessions=include_sessions)
        if not event:
            raise NotFoundError("Evento no encontrado")
        return event

    @staticmethod
    def list_events(
        db: Session,
        page: int = 1,
        per_page: int = 20,
        search: str | None = None,
        status: EventStatus | None = None,
    ) -> tuple[list[Event], dict]:
        """
        Lista eventos con filtros opcionales y paginación.

        Returns:
            Tuple[List[Event], Dict]: (eventos, metadata de paginación)
        """
        return crud_event.get_events(db, page=page, per_page=per_page, search=search, status=status)

    @staticmethod
    def create_event(db: Session, event_data: EventCreate, creator: User) -> Event:
        """
        Crea un nuevo evento

        Args:
            db: Sesión de base de datos
            event_data: Datos del evento a crear
            creator: Usuario que crea el evento

        Returns:
            Event: Evento creado
        """
        return crud_event.create_event(db=db, event=event_data, creator_id=creator.id)

    @staticmethod
    def update_event(db: Session, event_id: int, event_update: EventUpdate, user: User) -> Event:
        """
        Actualiza un evento con validaciones de negocio

        Raises:
            NotFoundError: Si el evento no existe
            ValidationError: Si las reglas de negocio no se cumplen
        """
        event = EventService.get_event(db, event_id, include_sessions=True)
        update_data = event_update.model_dump(exclude_unset=True)
        if "status" in update_data:
            status_value = update_data["status"]
            if isinstance(status_value, EventStatus):
                update_data["status"] = EventStatusDB(status_value.value)
        validate_event_update(event, update_data)

        updated_event = crud_event.update_event(
            db, event_id=event_id, event_update=EventUpdate(**update_data)
        )

        if not updated_event:
            raise ValidationError("Error al actualizar el evento")

        return updated_event

    @staticmethod
    def delete_event(db: Session, event_id: int, user: User) -> None:
        """
        Realiza soft delete de un evento y sus relaciones (cascada)

        Al eliminar un evento:
        - Se marca como eliminado (deleted_at)
        - Se eliminan (soft delete) todas sus sesiones
        - Se eliminan (soft delete) todos sus registros

        Raises:
            NotFoundError: Si el evento no existe
        """
        EventService.get_event(db, event_id)

        success = crud_event.soft_delete_event(db, event_id=event_id)
        if not success:
            raise ValidationError("Error al eliminar el evento")

    @staticmethod
    def get_user_events(
        db: Session, user: User, page: int = 1, per_page: int = 20
    ) -> tuple[list[Event], dict[str, Any]]:
        """
        Obtiene eventos creados por un usuario con paginación.

        Returns:
            Tuple[List[Event], Dict[str, Any]]: Lista de eventos y metadata de paginación
        """
        return crud_event.get_user_events(db, user_id=user.id, page=page, per_page=per_page)

    @staticmethod
    def verify_event_exists(db: Session, event_id: int) -> Event:
        """
        Verifica que el evento existe

        Raises:
            NotFoundError: Si el evento no existe

        Returns:
            Event: El evento encontrado
        """
        return EventService.get_event(db, event_id)
