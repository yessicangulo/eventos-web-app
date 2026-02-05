"""
Script para crear usuarios iniciales (admin y organizador)

Este script crea automáticamente un usuario administrador y un organizador
al iniciar el sistema por primera vez. Es idempotente: si los usuarios ya
existen, no los recrea.

Uso:
    # Desde Docker (automático con valores por defecto)
    python -m app.scripts.create_admin

    # Con variables de entorno
    ADMIN_EMAIL=admin@ejemplo.com ADMIN_PASSWORD=admin123 python -m app.scripts.create_admin

    # Con argumentos
    python -m app.scripts.create_admin --admin-email admin@ejemplo.com --organizer-email org@ejemplo.com
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import Session  # noqa: E402

from app.core.security import get_password_hash  # noqa: E402
from app.crud import user as crud_user  # noqa: E402
from app.database import SessionLocal  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402


def create_user_with_role(
    db: Session, email: str, password: str, role: UserRole, full_name: str = None
):
    """Crea un usuario con un rol específico (idempotente)"""
    existing_user = crud_user.get_user_by_email(db, email=email)
    if existing_user:
        if existing_user.role == role:
            print(f"✅ El usuario {email} ya existe con rol {role.value}")
            return existing_user
        else:
            existing_user.role = role
            db.commit()
            db.refresh(existing_user)
            print(f"✅ Usuario {email} actualizado a {role.value}")
            return existing_user

    hashed_password = get_password_hash(password)
    new_user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name or email.split("@")[0],
        role=role,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f"✅ Usuario {role.value.upper()} creado: {email}")
    return new_user


def create_initial_users(
    admin_email: str = None,
    admin_password: str = None,
    admin_name: str = None,
    organizer_email: str = None,
    organizer_password: str = None,
    organizer_name: str = None,
):
    """Crea usuarios iniciales (admin y organizador)"""
    db: Session = SessionLocal()
    try:
        print("🔐 Creando usuarios iniciales...")
        print("-" * 50)
        admin_email = admin_email or os.getenv("ADMIN_EMAIL", "admin@mis-eventos.com")
        admin_password = admin_password or os.getenv("ADMIN_PASSWORD", "admin123")
        admin_name = admin_name or os.getenv("ADMIN_NAME", "Administrador")

        organizer_email = organizer_email or os.getenv(
            "ORGANIZER_EMAIL", "organizer@mis-eventos.com"
        )
        organizer_password = organizer_password or os.getenv("ORGANIZER_PASSWORD", "organizer123")
        organizer_name = organizer_name or os.getenv("ORGANIZER_NAME", "Organizador")
        print(f"\n📧 Creando administrador: {admin_email}")
        create_user_with_role(db, admin_email, admin_password, UserRole.ADMIN, admin_name)
        print(f"\n📧 Creando organizador: {organizer_email}")
        create_user_with_role(
            db, organizer_email, organizer_password, UserRole.ORGANIZER, organizer_name
        )

        print("\n" + "=" * 50)
        print("✅ Usuarios iniciales creados exitosamente")
        print("=" * 50)
        print(f"\n👤 Admin: {admin_email} / {admin_password}")
        print(f"👤 Organizador: {organizer_email} / {organizer_password}")
        print("\n⚠️  IMPORTANTE: Cambia estas contraseñas en producción!")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error al crear usuarios: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Crear usuarios iniciales (admin y organizador)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python -m app.scripts.create_admin
  python -m app.scripts.create_admin --admin-email admin@ejemplo.com --admin-password admin123
  docker-compose exec backend python -m app.scripts.create_admin
        """,
    )

    parser.add_argument("--admin-email", help="Email del administrador")
    parser.add_argument("--admin-password", help="Contraseña del administrador")
    parser.add_argument("--admin-name", help="Nombre del administrador")
    parser.add_argument("--organizer-email", help="Email del organizador")
    parser.add_argument("--organizer-password", help="Contraseña del organizador")
    parser.add_argument("--organizer-name", help="Nombre del organizador")

    args = parser.parse_args()

    try:
        create_initial_users(
            admin_email=args.admin_email,
            admin_password=args.admin_password,
            admin_name=args.admin_name,
            organizer_email=args.organizer_email,
            organizer_password=args.organizer_password,
            organizer_name=args.organizer_name,
        )
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
