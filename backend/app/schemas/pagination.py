"""
Schemas generales de paginación para reutilizar en toda la API
"""

from typing import Generic, TypeVar

from pydantic import BaseModel, field_validator

from app.core.validators import validate_page, validate_per_page

T = TypeVar("T")


class PaginationQueryParams(BaseModel):
    """
    Schema general para parámetros de paginación en query params.
    Reutilizable en cualquier endpoint que necesite paginación.
    """

    page: int = 1
    per_page: int = 20

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


class PaginationMetadata(BaseModel):
    """
    Schema general para metadata de paginación en respuestas.
    Reutilizable en cualquier respuesta paginada.
    """

    page: int
    per_page: int
    total_count: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Schema genérico para respuestas paginadas.

    Usage:
        class EventListResponse(PaginatedResponse[EventResponse]):
            items: List[EventResponse]  # Renombrar 'items' según necesidad

        O usar directamente:
        PaginatedResponse[EventResponse](items=events, pagination=metadata)
    """

    items: list[T]
    pagination: PaginationMetadata
