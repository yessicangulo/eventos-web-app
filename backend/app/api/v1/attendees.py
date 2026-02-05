from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.attendee import EventAttendeesResponse, MyEventsListResponse
from app.schemas.pagination import PaginationQueryParams
from app.services.attendee_service import AttendeeService

router = APIRouter()


@router.post(
    "/register/{event_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Registrarse a un evento",
    description="Registra al usuario actual a un evento (requiere rol ATTENDEE)",
)
def register_to_event(
    event_id: int,
    current_user: User = Depends(require_roles(UserRole.ATTENDEE)),
    db: Session = Depends(get_db),
):
    """Registrarse a un evento"""
    registration = AttendeeService.register_to_event(db, event_id, current_user)
    return {
        "message": "Registrado exitosamente al evento",
        "data": {"event_id": event_id, "registered_at": registration.registered_at.isoformat()},
    }


@router.delete(
    "/unregister/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancelar registro a un evento",
    description="Cancela el registro del usuario actual a un evento",
)
def unregister_from_event(
    event_id: int,
    current_user: User = Depends(require_roles(UserRole.ATTENDEE)),
    db: Session = Depends(get_db),
):
    """Cancelar registro a un evento"""
    AttendeeService.unregister_from_event(db, event_id, current_user)


@router.get(
    "/my-events",
    response_model=MyEventsListResponse,
    summary="Obtener mis eventos registrados",
    description="Obtiene la lista paginada de eventos a los que el usuario actual está registrado (requiere rol ATTENDEE)",
)
def get_my_registered_events(
    params: PaginationQueryParams = Depends(),
    current_user: User = Depends(require_roles(UserRole.ATTENDEE)),
    db: Session = Depends(get_db),
):
    """Obtener eventos a los que estoy registrado con paginación"""
    from app.schemas.event import EventResponse
    from app.schemas.pagination import PaginationMetadata

    events, pagination_metadata = AttendeeService.get_user_registered_events(
        db, current_user, page=params.page, per_page=params.per_page
    )

    return MyEventsListResponse(
        events=[EventResponse.model_validate(event) for event in events],
        pagination=PaginationMetadata(**pagination_metadata),
    )


@router.get(
    "/event/{event_id}/attendees",
    response_model=EventAttendeesResponse,
    summary="Obtener asistentes de un evento",
    description="Obtiene la lista de asistentes de un evento (requiere rol ORGANIZER)",
)
def get_event_attendees(
    event_id: int,
    current_user: User = Depends(require_roles(UserRole.ORGANIZER)),
    db: Session = Depends(get_db),
):
    """Obtener lista de asistentes de un evento"""
    result = AttendeeService.get_event_attendees(db, event_id, current_user)
    return result


@router.get(
    "/check/{event_id}",
    summary="Verificar registro en evento",
    description="Verifica si el usuario actual está registrado en un evento",
)
def check_registration(
    event_id: int,
    current_user: User = Depends(require_roles(UserRole.ATTENDEE)),
    db: Session = Depends(get_db),
):
    """Verificar si estoy registrado en un evento"""
    is_registered = AttendeeService.check_registration(db, event_id, current_user)
    return {"is_registered": is_registered}
