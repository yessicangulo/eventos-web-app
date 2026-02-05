from datetime import datetime

from pydantic import BaseModel, model_validator

from app.schemas.pagination import PaginationMetadata


class SessionBase(BaseModel):
    title: str
    description: str | None = None
    speaker_name: str | None = None
    speaker_bio: str | None = None
    start_time: datetime
    end_time: datetime
    location: str | None = None
    capacity: int | None = None

    @model_validator(mode="after")
    def end_time_after_start_time(self):
        if self.end_time <= self.start_time:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio")
        return self


class SessionCreate(SessionBase):
    event_id: int


class SessionUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    speaker_name: str | None = None
    speaker_bio: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    location: str | None = None
    capacity: int | None = None


class SessionResponse(SessionBase):
    id: int
    event_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SessionListResponse(BaseModel):
    """Respuesta de lista de sesiones con paginación"""

    sessions: list[SessionResponse]
    pagination: PaginationMetadata
