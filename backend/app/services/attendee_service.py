"""
Servicio de asistentes - Lógica de negocio para registro a eventos
"""

from typing import Any

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.crud import attendee as crud_attendee
from app.models.attendee import EventRegistration
from app.models.user import User
from app.schemas.attendee import AttendeeInfo, EventAttendeesResponse
from app.services.event_service import EventService


class AttendeeService:
    """Servicio para operaciones relacionadas con asistentes"""

    @staticmethod
    def register_to_event(db: Session, event_id: int, user: User) -> EventRegistration:
        """
        Registra un usuario a un evento

        Raises:
            NotFoundError: Si el evento no existe
            ValidationError: Si el evento está lleno
            ConflictError: Si el usuario ya está registrado
        """
        event = EventService.get_event(db, event_id)
        if event.is_full:
            raise ValidationError("El evento está lleno")
        is_registered = crud_attendee.is_user_registered(db, user_id=user.id, event_id=event_id)

        if is_registered:
            raise ConflictError("Ya estás registrado en este evento")
        registration = crud_attendee.register_to_event(db, user_id=user.id, event_id=event_id)

        return registration

    @staticmethod
    def unregister_from_event(db: Session, event_id: int, user: User) -> None:
        """
        Cancela el registro de un usuario a un evento

        Raises:
            NotFoundError: Si el usuario no está registrado
        """
        success = crud_attendee.unregister_from_event(db, user_id=user.id, event_id=event_id)

        if not success:
            raise NotFoundError("No estás registrado en este evento")

    @staticmethod
    def get_user_registered_events(
        db: Session, user: User, page: int = 1, per_page: int = 20
    ) -> tuple[list, dict[str, Any]]:
        """
        Obtiene eventos a los que el usuario está registrado con paginación.
        Usa JOIN para traer los eventos directamente en una sola query.

        Returns:
            Tuple[List[Event], Dict[str, Any]]: Lista de eventos y metadata de paginación
        """
        return crud_attendee.get_user_registered_events(
            db, user_id=user.id, page=page, per_page=per_page
        )

    @staticmethod
    def get_event_attendees(db: Session, event_id: int, user: User) -> EventAttendeesResponse:
        """
        Obtiene lista de asistentes de un evento

        Raises:
            NotFoundError: Si el evento no existe

        Returns:
            EventAttendeesResponse: Información de asistentes
        """
        event = EventService.verify_event_exists(db, event_id)

        registrations = crud_attendee.get_event_registrations(db, event_id=event_id)

        return EventAttendeesResponse(
            event_id=event_id,
            total_attendees=len(registrations),
            capacity=event.capacity,
            available=event.available_capacity,
            attendees=[
                AttendeeInfo(
                    user_id=reg.user_id,
                    email=reg.user.email,
                    full_name=reg.user.full_name,
                    registered_at=reg.registered_at,
                )
                for reg in registrations
            ],
        )

    @staticmethod
    def check_registration(db: Session, event_id: int, user: User) -> bool:
        """
        Verifica si un usuario está registrado en un evento

        Returns:
            bool: True si está registrado, False si no
        """
        is_registered = crud_attendee.is_user_registered(db, user_id=user.id, event_id=event_id)

        return is_registered
