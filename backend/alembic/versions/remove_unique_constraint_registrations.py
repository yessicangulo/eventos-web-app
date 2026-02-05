"""remove unique constraint from event_registrations

Revision ID: remove_unique_constraint
Revises: add_soft_delete_fields
Create Date: 2026-02-05 02:30:00.000000

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "remove_unique_constraint"
down_revision = "add_soft_delete_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Eliminar el constraint único si existe (para bases de datos existentes)
    # La validación de duplicados se maneja en el código, no en la BD
    # Esto permite soft delete sin problemas
    try:
        op.drop_constraint("unique_user_event_registration", "event_registrations", type_="unique")
    except Exception:
        # Si no existe, no pasa nada (para nuevas bases de datos)
        pass


def downgrade() -> None:
    # Restaurar el constraint único (opcional, solo si se necesita)
    # op.create_unique_constraint(
    #     'unique_user_event_registration',
    #     'event_registrations',
    #     ['user_id', 'event_id']
    # )
    pass
