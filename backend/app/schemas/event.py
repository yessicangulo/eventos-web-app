from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, field_validator, model_validator

from app.core.validators import validate_page, validate_per_page, validate_search
from app.models.event import EventStatus

if TYPE_CHECKING:
    from app.schemas.session import SessionResponse


class EventBase(BaseModel):
    name: str
    description: str | None = None
    location: str | None = None
    start_date: datetime
    end_date: datetime
    capacity: int

    @field_validator("capacity")
    @classmethod
    def capacity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")
        return v

    @model_validator(mode="after")
    def end_date_after_start_date(self):
        if self.end_date <= self.start_date:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio")
        return self


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    location: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    capacity: int | None = None
    status: EventStatus | None = None  # Se acepta EventStatus pero se valida que sea de BD

    @field_validator("status")
    @classmethod
    def status_must_be_db_status(cls, v):
        """Solo se pueden actualizar a estados que se guardan en BD (manuales)"""
        if v is not None:
            # Permitir EventStatus pero validar que sea uno de los estados de BD
            # No permitir ONGOING ni COMPLETED (son calculados automáticamente)
            valid_db_statuses = {EventStatus.SCHEDULED, EventStatus.CANCELLED}
            if v not in valid_db_statuses:
                raise ValueError(
                    f"El estado {v} no puede ser guardado en BD. "
                    f"Solo se permiten: SCHEDULED, CANCELLED. "
                    f"Los estados ONGOING y COMPLETED se calculan automáticamente."
                )
        return v


class EventResponse(EventBase):
    id: int
    computed_status: EventStatus  # Estado computado (usa computed_status del modelo)
    creator_id: int
    created_at: datetime
    available_capacity: int
    is_full: bool

    class Config:
        from_attributes = True


class EventListQueryParams(BaseModel):
    """
    Schema para validar los parámetros de query del endpoint GET /events

    Parámetros:
        page (int, opcional): Número de página (1-indexed). Default: 1
            Ejemplo: page=2 significa "segunda página"
            Uso: Para paginación, más intuitivo que skip/limit

        per_page (int, opcional): Número de resultados por página. Default: 20, Max: 100
            Ejemplo: per_page=20 significa "20 eventos por página"
            Uso: Controla cuántos resultados quieres ver por página
            Nota: Máximo 100 para evitar sobrecargar el servidor

        search (str, opcional): Texto para buscar eventos por nombre (búsqueda parcial, case-insensitive)
            Ejemplo: search="conferencia" encontrará "Conferencia de Python", "Conferencia Tech", etc.
            Uso: Búsqueda avanzada por nombre o parte del nombre (requerimiento)
            Nota: Busca en el campo 'name' del evento, no distingue mayúsculas/minúsculas

        status (EventStatus, opcional): Filtrar eventos por estado computado
            Valores válidos: SCHEDULED, ONGOING, COMPLETED, CANCELLED
            Ejemplo: status=ONGOING → solo eventos en progreso
            Uso: Filtrar eventos según su estado computado (computed_status)
            Nota: El filtro se aplica sobre el estado computado, no el estado manual en BD
    """

    page: int = 1
    per_page: int = 20
    search: str | None = None
    status: EventStatus | None = None

    @field_validator("page")
    @classmethod
    def page_must_be_positive(cls, v):
        """page debe ser >= 1"""
        return validate_page(v)

    @field_validator("per_page")
    @classmethod
    def per_page_must_be_valid(cls, v):
        """per_page debe ser > 0 y <= 100"""
        return validate_per_page(v)

    @field_validator("search")
    @classmethod
    def search_must_not_be_empty(cls, v):
        """Si se proporciona search, no debe estar vacío"""
        return validate_search(v)


class EventDetailResponse(EventResponse):
    """Schema detallado con sesiones incluidas (para GET /events/<id>)"""

    sessions: list["SessionResponse"] = []

    class Config:
        from_attributes = True


# Importar PaginationMetadata del schema general
from app.schemas.pagination import PaginationMetadata  # noqa: E402


class EventListResponse(BaseModel):
    """Respuesta de lista de eventos con paginación"""

    events: list[EventResponse]
    pagination: PaginationMetadata


# Resolver forward reference después de que ambos módulos estén cargados
if not TYPE_CHECKING:
    from app.schemas.session import SessionResponse

    EventDetailResponse.model_rebuild()
