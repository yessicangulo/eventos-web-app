from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import (
    UserAdminCreate,
    UserAdminUpdate,
    UserListQueryParams,
    UserListResponse,
    UserResponse,
)
from app.services.user_service import UserService

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Crea un nuevo usuario. Solo ADMIN puede crear usuarios. No se pueden crear usuarios admin desde este endpoint.",
)
def create_user(
    user_data: UserAdminCreate,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    """
    Crear usuario (solo ADMIN).
    Puede crear organizadores o asistentes, pero NO administradores.
    Para crear administradores, use el script de inicialización.
    """
    if user_data.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No se pueden crear usuarios admin desde este endpoint. Use el script de inicialización: python -m app.scripts.create_admin",
        )

    new_user = UserService.create_user_with_role(
        db,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name,
        role=user_data.role,
        is_active=user_data.is_active,
    )
    return UserResponse.model_validate(new_user)


@router.get(
    "/",
    response_model=UserListResponse,
    summary="Listar usuarios",
    description="Lista todos los usuarios con filtros opcionales y paginación (requiere rol ADMIN)",
)
def list_users(
    params: UserListQueryParams = Depends(),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    """Listar todos los usuarios con filtros opcionales y paginación"""
    users, pagination_metadata = UserService.list_users(
        db,
        page=params.page,
        per_page=params.per_page,
        search=params.search,
        role=params.role,
        is_active=params.is_active,
    )

    return UserListResponse(users=users, pagination=pagination_metadata)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener detalle de usuario",
    description="Obtiene el detalle de un usuario específico (requiere rol ADMIN)",
)
def get_user(
    user_id: int,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    """Obtener detalle de un usuario"""
    user = UserService.get_user_by_id(db, user_id)
    return UserResponse.model_validate(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario",
    description="Actualiza un usuario (cambiar rol, activar/desactivar, etc.) (requiere rol ADMIN)",
)
def update_user(
    user_id: int,
    user_data: UserAdminUpdate,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    """Actualizar un usuario (cambiar rol, activar/desactivar, etc.)"""
    updated_user = UserService.update_user(
        db,
        user_id,
        user_data,
    )
    return UserResponse.model_validate(updated_user)
