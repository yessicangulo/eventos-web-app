"""add soft delete fields

Revision ID: add_soft_delete_fields
Revises: 24530a0a489e
Create Date: 2026-02-04 23:00:00.000000

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "add_soft_delete_fields"
down_revision = "24530a0a489e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Agregar campos de soft delete a events
    op.add_column("events", sa.Column("deleted_at", sa.DateTime(), nullable=True))
    op.add_column(
        "events", sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="false")
    )

    # Agregar campos de soft delete y updated_at a sessions
    op.add_column("sessions", sa.Column("deleted_at", sa.DateTime(), nullable=True))
    op.add_column(
        "sessions", sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="false")
    )
    # Para updated_at, primero agregamos como nullable, luego actualizamos valores existentes, luego hacemos NOT NULL
    op.add_column("sessions", sa.Column("updated_at", sa.DateTime(), nullable=True))
    op.execute("UPDATE sessions SET updated_at = created_at WHERE updated_at IS NULL")
    op.alter_column("sessions", "updated_at", nullable=False)

    # Agregar campos de soft delete a event_registrations
    op.add_column("event_registrations", sa.Column("deleted_at", sa.DateTime(), nullable=True))
    op.add_column(
        "event_registrations",
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default="false"),
    )


def downgrade() -> None:
    # Eliminar campos de soft delete de event_registrations
    op.drop_column("event_registrations", "is_deleted")
    op.drop_column("event_registrations", "deleted_at")

    # Eliminar campos de soft delete y updated_at de sessions
    op.drop_column("sessions", "updated_at")
    op.drop_column("sessions", "is_deleted")
    op.drop_column("sessions", "deleted_at")

    # Eliminar campos de soft delete de events
    op.drop_column("events", "is_deleted")
    op.drop_column("events", "deleted_at")
