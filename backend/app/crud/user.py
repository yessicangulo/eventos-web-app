from datetime import datetime
from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.db_utils import save_and_refresh, update_and_refresh
from app.core.pagination import apply_pagination, get_pagination_metadata
from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserRole
from app.schemas.user import UserAdminUpdate, UserCreate


def get_user(db: Session, user_id: int) -> User | None:
    """Obtiene usuario por ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Obtiene usuario por email"""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    """Crea un nuevo usuario"""
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, full_name=user.full_name)
    return save_and_refresh(db, db_user)


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Autentica un usuario"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_users(
    db: Session,
    page: int = 1,
    per_page: int = 20,
    search: str | None = None,
    role: UserRole | None = None,
    is_active: bool | None = None,
) -> tuple[list[User], dict[str, Any]]:
    """
    Lista usuarios con filtros opcionales y paginación.

    Returns:
        Tuple[List[User], Dict]: (usuarios, metadata de paginación)
    """
    query = db.query(User)

    if search:
        query = query.filter(
            or_(User.email.ilike(f"%{search}%"), User.full_name.ilike(f"%{search}%"))
        )

    if role:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    pagination_metadata = get_pagination_metadata(query, page=page, per_page=per_page)

    query = apply_pagination(query, page=page, per_page=per_page)

    users = query.all()

    return users, pagination_metadata


def create_user_with_role(
    db: Session,
    email: str,
    password: str,
    full_name: str | None = None,
    role: UserRole = UserRole.ATTENDEE,
    is_active: bool = True,
) -> User:
    """Crea un nuevo usuario con un rol específico"""
    hashed_password = get_password_hash(password)
    db_user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        role=role,
        is_active=is_active,
    )
    return save_and_refresh(db, db_user)


def update_user(db: Session, user_id: int, user_update: UserAdminUpdate) -> User | None:
    """Actualiza un usuario"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db_user.updated_at = datetime.utcnow()
    return update_and_refresh(db, db_user)
