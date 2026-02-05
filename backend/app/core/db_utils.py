"""
Utilidades para manejo de base de datos - Helpers reutilizables
"""

from datetime import datetime
from typing import TypeVar

from sqlalchemy.orm import Session

T = TypeVar("T")


def save_and_refresh(db: Session, instance: T, refresh: bool = True) -> T:
    """
    Guarda una instancia en la base de datos y la refresca

    Args:
        db: Sesión de base de datos
        instance: Instancia del modelo a guardar
        refresh: Si True, refresca la instancia después del commit

    Returns:
        La instancia guardada (y refrescada si refresh=True)
    """
    db.add(instance)
    db.commit()
    if refresh:
        db.refresh(instance)
    return instance


def update_and_refresh(db: Session, instance: T, refresh: bool = True) -> T:
    """
    Actualiza una instancia existente y la refresca

    Args:
        db: Sesión de base de datos
        instance: Instancia del modelo a actualizar
        refresh: Si True, refresca la instancia después del commit

    Returns:
        La instancia actualizada (y refrescada si refresh=True)
    """
    db.commit()
    if refresh:
        db.refresh(instance)
    return instance


def soft_delete(db: Session, instance: T, refresh: bool = True) -> T:
    """
    Realiza soft delete de una instancia (marca deleted_at e is_deleted)

    Args:
        db: Sesión de base de datos
        instance: Instancia del modelo a eliminar (soft delete)
        refresh: Si True, refresca la instancia después del commit

    Returns:
        La instancia con deleted_at e is_deleted actualizados
    """
    now = datetime.utcnow()

    if hasattr(instance, "deleted_at"):
        instance.deleted_at = now
    if hasattr(instance, "is_deleted"):
        instance.is_deleted = True
    if hasattr(instance, "updated_at"):
        instance.updated_at = now

    db.commit()
    if refresh:
        db.refresh(instance)
    return instance
