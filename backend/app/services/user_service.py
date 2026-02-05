"""
Servicio de usuarios - Lógica de negocio para autenticación y gestión de usuarios
"""

from typing import Any

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ValidationError
from app.crud import user as crud_user
from app.models.user import User, UserRole
from app.schemas.user import UserAdminUpdate, UserCreate


class UserService:
    """Servicio para operaciones relacionadas con usuarios"""

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Obtiene un usuario por ID"""
        user = crud_user.get_user(db, user_id=user_id)
        if not user:
            raise NotFoundError("Usuario no encontrado")
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """Obtiene un usuario por email"""
        return crud_user.get_user_by_email(db, email=email)

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        """
        Registra un nuevo usuario

        Raises:
            ValidationError: Si el email ya está registrado
        """
        existing_user = crud_user.get_user_by_email(db, email=user_data.email)
        if existing_user:
            raise ValidationError("El email ya está registrado")

        return crud_user.create_user(db=db, user=user_data)

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """
        Autentica un usuario

        Raises:
            ValidationError: Si las credenciales son incorrectas
        """
        user = crud_user.authenticate_user(db, email, password)
        if not user:
            raise ValidationError("Email o contraseña incorrectos")
        return user

    @staticmethod
    def list_users(
        db: Session,
        page: int = 1,
        per_page: int = 20,
        search: str | None = None,
        role: UserRole | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[User], dict[str, Any]]:
        """
        Lista usuarios con filtros opcionales y paginación.
        Solo ADMIN puede usar este método.

        Returns:
            Tuple[List[User], Dict]: (usuarios, metadata de paginación)
        """
        return crud_user.get_users(
            db, page=page, per_page=per_page, search=search, role=role, is_active=is_active
        )

    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        user_update: UserAdminUpdate,
    ) -> User:
        """
        Actualiza un usuario (solo ADMIN)

        Raises:
            NotFoundError: Si el usuario no existe
        """

        UserService.get_user_by_id(db, user_id)

        updated_user = crud_user.update_user(db, user_id=user_id, user_update=user_update)

        if not updated_user:
            raise ValidationError("Error al actualizar el usuario")

        return updated_user

    @staticmethod
    def create_user_with_role(
        db: Session,
        email: str,
        password: str,
        full_name: str | None = None,
        role: UserRole = UserRole.ATTENDEE,
        is_active: bool = True,
    ) -> User:
        """
        Crea un nuevo usuario con un rol específico (solo ADMIN puede usar esto)

        Raises:
            ValidationError: Si el email ya está registrado
        """
        existing_user = crud_user.get_user_by_email(db, email=email)
        if existing_user:
            raise ValidationError("El email ya está registrado")

        return crud_user.create_user_with_role(
            db=db,
            email=email,
            password=password,
            full_name=full_name,
            role=role,
            is_active=is_active,
        )
