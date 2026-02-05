"""
Dependencies de FastAPI para autenticación y autorización
"""

from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.crud import user as crud_user
from app.database import get_db
from app.models.user import User, UserRole

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)
) -> User:
    """
    Dependency para obtener el usuario actual autenticado.
    Valida el token JWT y retorna el usuario.
    """
    token = credentials.credentials
    email = decode_access_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = crud_user.get_user_by_email(db, email=email)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_roles(*allowed_roles: UserRole) -> Callable:
    """
    Factory function que crea un dependency para validar roles.

    Args:
        *allowed_roles: Uno o más roles permitidos

    Returns:
        Dependency function que valida el rol del usuario

    Usage:
        @router.get("/")
        def my_endpoint(current_user: User = Depends(require_roles(UserRole.ORGANIZER))):
            ...
    """

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role == UserRole.ADMIN:
            return current_user
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción",
            )
        return current_user

    return role_checker
