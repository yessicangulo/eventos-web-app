from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, EmailStr, field_validator

from app.core.validators import validate_page, validate_per_page, validate_search
from app.models.user import UserRole

if TYPE_CHECKING:
    from app.schemas.event import EventResponse


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserAdminCreate(BaseModel):
    """Schema para crear usuario por ADMIN (incluye password y role)"""

    email: EmailStr
    password: str
    full_name: str | None = None
    role: UserRole = UserRole.ATTENDEE  # Por defecto attendee, admin puede cambiar a organizer
    is_active: bool = True


class UserAdminUpdate(BaseModel):
    """Schema para actualizar usuario por ADMIN"""

    full_name: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserProfileResponse(UserResponse):
    """Perfil completo del usuario con eventos registrados"""

    registered_events: list["EventResponse"] = []
    created_events_count: int = 0

    class Config:
        from_attributes = True


class UserListQueryParams(BaseModel):
    """Parámetros de query para listar usuarios"""

    page: int = 1
    per_page: int = 20
    search: str | None = None  # Búsqueda por email o nombre
    role: UserRole | None = None  # Filtrar por rol
    is_active: bool | None = None  # Filtrar por estado activo

    @field_validator("page")
    @classmethod
    def page_must_be_positive(cls, v):
        return validate_page(v)

    @field_validator("per_page")
    @classmethod
    def per_page_must_be_valid(cls, v):
        return validate_per_page(v)

    @field_validator("search")
    @classmethod
    def search_must_not_be_empty(cls, v):
        """Si se proporciona search, no debe estar vacío"""
        return validate_search(v)


from app.schemas.pagination import PaginationMetadata  # noqa: E402


class UserListResponse(BaseModel):
    """Respuesta de lista de usuarios con paginación"""

    users: list[UserResponse]
    pagination: PaginationMetadata


# Resolver forward reference
if not TYPE_CHECKING:
    from app.schemas.event import EventResponse

    UserProfileResponse.model_rebuild()
