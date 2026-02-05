"""
Validaciones de negocio para eventos
Reglas de edición y transiciones de estado
"""

from datetime import datetime

from app.core.exceptions import ValidationError
from app.models.event import Event, EventStatus, EventStatusDB


def _get_max_session_capacity(event: Event) -> int | None:
    """
    Obtiene la máxima capacidad de las sesiones del evento.

    Args:
        event: El evento a verificar

    Returns:
        La máxima capacidad de las sesiones, o None si ninguna sesión tiene capacidad definida
    """
    if not event.sessions:
        return None

    capacities = [
        session.capacity
        for session in event.sessions
        if session.capacity is not None and session.deleted_at is None and not session.is_deleted
    ]
    if not capacities:
        return None

    return max(capacities)


def validate_field_editable_by_status(event: Event, field_name: str, new_value: any = None) -> None:
    """
    Valida si un campo puede ser editado según el estado computado del evento.

    Args:
        event: El evento a validar
        field_name: Nombre del campo a validar
        new_value: Nuevo valor (opcional, para validaciones específicas)

    Raises:
        ValidationError: Si el campo no puede ser editado en el estado actual
    """
    computed_status = event.computed_status
    now = datetime.utcnow()
    if computed_status == EventStatus.SCHEDULED:
        if field_name in ["name", "description", "location"]:
            return
        if field_name in ["start_date", "end_date"]:
            if now >= event.start_date:
                raise ValidationError(
                    f"No se puede modificar {field_name} porque el evento ya ha iniciado"
                )
            return
        if field_name == "capacity":
            if new_value is not None:
                registered_count = len(
                    [r for r in event.registrations if r.deleted_at is None and not r.is_deleted]
                )
                if new_value < registered_count:
                    raise ValidationError(
                        f"No se puede establecer la capacidad a {new_value} porque hay {registered_count} usuarios registrados. "
                        f"La capacidad mínima debe ser {registered_count}."
                    )
                max_session_capacity = _get_max_session_capacity(event)
                if max_session_capacity is not None and new_value < max_session_capacity:
                    raise ValidationError(
                        f"No se puede establecer la capacidad a {new_value} porque hay sesiones con capacidad de {max_session_capacity}. "
                        f"La capacidad mínima del evento debe ser {max_session_capacity}."
                    )
            return
        if field_name == "status":
            return

        raise ValidationError(
            f"El campo '{field_name}' no puede ser editado cuando el evento está en estado SCHEDULED"
        )
    if computed_status == EventStatus.ONGOING:
        if field_name in ["description", "location"]:
            return
        if field_name in ["name", "start_date", "end_date", "capacity", "status"]:
            raise ValidationError(
                f"El campo '{field_name}' no puede ser editado cuando el evento está en progreso (ONGOING)"
            )
        return
    if computed_status == EventStatus.COMPLETED:
        raise ValidationError(
            f"El campo '{field_name}' no puede ser editado cuando el evento está completado (COMPLETED)"
        )
    if computed_status == EventStatus.CANCELLED:
        if field_name == "status":
            return
        raise ValidationError(
            f"El campo '{field_name}' no puede ser editado cuando el evento está cancelado (CANCELLED). "
            f"Solo se puede reactivar el evento cambiando el estado a SCHEDULED (si el evento no ha iniciado)."
        )


def validate_status_transition(event: Event, new_status: EventStatusDB) -> None:
    """
    Valida si una transición de estado es permitida.

    Transiciones permitidas:
    - SCHEDULED → CANCELLED
    - CANCELLED → SCHEDULED (solo si el evento no ha iniciado)

    Transiciones NO permitidas:
    - No se pueden asignar ONGOING o COMPLETED manualmente (son calculados automáticamente)
    - COMPLETED → cualquier otro
    - CANCELLED → cualquier otro (excepto reactivar a SCHEDULED si no ha iniciado)

    Args:
        event: El evento actual
        new_status: El nuevo estado a asignar

    Raises:
        ValidationError: Si la transición no está permitida
    """
    current_status = event.status
    computed_status = event.computed_status
    if current_status == new_status:
        return

    # No permitir asignar estados calculados automáticamente
    if new_status not in [EventStatusDB.SCHEDULED, EventStatusDB.CANCELLED]:
        raise ValidationError(
            f"No se puede asignar el estado {new_status.value} manualmente. "
            f"Los estados ONGOING y COMPLETED se calculan automáticamente basados en las fechas."
        )
    if current_status == EventStatusDB.SCHEDULED and new_status == EventStatusDB.CANCELLED:
        return
    if computed_status == EventStatus.COMPLETED:
        raise ValidationError("No se puede cambiar el estado de un evento completado")
    if current_status == EventStatusDB.CANCELLED:
        if new_status == EventStatusDB.SCHEDULED:
            now = datetime.utcnow()
            if now < event.start_date:
                return
            else:
                raise ValidationError(
                    "No se puede reactivar un evento cancelado que ya ha iniciado"
                )
        else:
            raise ValidationError(
                f"No se puede cambiar el estado de un evento cancelado a {new_status.value}. "
                f"Solo se puede reactivar a SCHEDULED si el evento no ha iniciado."
            )

    # No permitir transiciones inválidas
    raise ValidationError(
        f"No se permite la transición de estado de {current_status.value} a {new_status.value}"
    )


def validate_event_update(event: Event, update_data: dict) -> None:
    """
    Valida todas las reglas de negocio para actualizar un evento.

    Args:
        event: El evento actual
        update_data: Diccionario con los campos a actualizar

    Raises:
        ValidationError: Si alguna validación falla
    """
    if "status" in update_data:
        new_status = update_data["status"]
        if isinstance(new_status, EventStatus):
            new_status = EventStatusDB(new_status.value)
        validate_status_transition(event, new_status)
    for field_name, new_value in update_data.items():
        if field_name == "status":
            continue  # Ya validado arriba
        validate_field_editable_by_status(event, field_name, new_value)
