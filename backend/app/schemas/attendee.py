"""
Schemas para asistentes y registros a eventos
"""

from datetime import datetime

from pydantic import BaseModel

from app.schemas.event import EventResponse
from app.schemas.pagination import PaginationMetadata


class EventRegistrationCreate(BaseModel):
    """Schema para crear un registro a un evento"""

    event_id: int


class EventRegistrationResponse(BaseModel):
    """Schema para respuesta de registro a evento"""

    id: int
    user_id: int
    event_id: int
    registered_at: datetime

    class Config:
        from_attributes = True


class EventRegistrationWithEvent(BaseModel):
    """Schema para registro con información del evento"""

    id: int
    user_id: int
    event_id: int
    registered_at: datetime
    event: EventResponse

    class Config:
        from_attributes = True


class AttendeeInfo(BaseModel):
    """Información de un asistente"""

    user_id: int
    email: str
    full_name: str | None = None
    registered_at: datetime


class EventAttendeesResponse(BaseModel):
    """Respuesta con lista de asistentes de un evento"""

    event_id: int
    total_attendees: int
    capacity: int | None = None
    available: int
    attendees: list[AttendeeInfo]


class MyEventsListResponse(BaseModel):
    """Respuesta de lista de eventos registrados por el usuario con paginación"""

    events: list[EventResponse]
    pagination: PaginationMetadata
