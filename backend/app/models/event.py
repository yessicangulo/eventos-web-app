import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy import (
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship

from app.database import Base


class EventStatusDB(str, enum.Enum):
    """Estados que se pueden guardar en la base de datos (solo manuales)"""

    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"


class EventStatus(str, enum.Enum):
    """Estados del evento para respuestas (incluye calculados)"""

    SCHEDULED = "scheduled"
    ONGOING = "ongoing"  # Calculado dinámicamente
    COMPLETED = "completed"  # Calculado dinámicamente
    CANCELLED = "cancelled"


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(SQLEnum(EventStatusDB), default=EventStatusDB.SCHEDULED, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True, default=None)  # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=False)  # Soft delete (boolean)

    # Relaciones
    creator = relationship("User", back_populates="created_events", foreign_keys=[creator_id])
    sessions = relationship(
        "Session",
        back_populates="event",
        cascade="all, delete-orphan",
        primaryjoin="and_(Event.id == foreign(Session.event_id), Session.deleted_at.is_(None), Session.is_deleted == False)",
        lazy="select",
    )
    registrations = relationship(
        "EventRegistration",
        back_populates="event",
        cascade="all, delete-orphan",
        primaryjoin="and_(Event.id == foreign(EventRegistration.event_id), EventRegistration.deleted_at.is_(None), EventRegistration.is_deleted == False)",
        lazy="select",
    )

    @property
    def available_capacity(self):
        """Calcula la capacidad disponible (solo registros no eliminados)"""
        registered = len(
            [r for r in self.registrations if r.deleted_at is None and not r.is_deleted]
        )
        return max(0, self.capacity - registered)

    @property
    def is_full(self):
        """Verifica si el evento está lleno (solo registros no eliminados)"""
        return self.available_capacity == 0

    @property
    def computed_status(self) -> EventStatus:
        """
        Calcula el estado real del evento basado en fechas y estado manual.

        Reglas:
        - Si status es CANCELLED: retorna ese estado (manual)
        - Si status es SCHEDULED: calcula dinámicamente basado en fechas:
          * Si ya pasó end_date → COMPLETED
          * Si está entre start_date y end_date → ONGOING
          * Si aún no ha empezado → SCHEDULED (programado)

        Returns:
            EventStatus: El estado computado real del evento
        """
        # Estado manual: retornar tal cual (convertir a EventStatus)
        if self.status == EventStatusDB.CANCELLED:
            return EventStatus.CANCELLED

        # Si es SCHEDULED, calcular dinámicamente basado en fechas
        if self.status == EventStatusDB.SCHEDULED:
            now = datetime.utcnow()

            # Si ya pasó la fecha de fin → COMPLETED
            if now > self.end_date:
                return EventStatus.COMPLETED

            # Si está entre inicio y fin → ONGOING
            if self.start_date <= now <= self.end_date:
                return EventStatus.ONGOING

            # Si aún no ha empezado → SCHEDULED (programado)
            return EventStatus.SCHEDULED

        # Fallback: retornar el estado actual convertido
        return EventStatus(self.status.value)
