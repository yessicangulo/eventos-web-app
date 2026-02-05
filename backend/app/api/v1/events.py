from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.event import (
    EventCreate,
    EventDetailResponse,
    EventListQueryParams,
    EventListResponse,
    EventResponse,
    EventUpdate,
)
from app.schemas.pagination import PaginationMetadata, PaginationQueryParams
from app.services.event_service import EventService

router = APIRouter()


@router.get(
    "/",
    response_model=EventListResponse,
    summary="Listar eventos",
    description="Lista todos los eventos con filtros opcionales y paginación",
)
def list_events(params: EventListQueryParams = Depends(), db: Session = Depends(get_db)):
    """Listar todos los eventos con filtros opcionales y paginación"""
    events, pagination_metadata = EventService.list_events(
        db, page=params.page, per_page=params.per_page, search=params.search, status=params.status
    )

    return EventListResponse(events=events, pagination=pagination_metadata)


@router.get(
    "/{event_id}",
    response_model=EventDetailResponse,
    summary="Obtener detalle de evento",
    description="Obtiene el detalle de un evento con sesiones incluidas",
)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Obtener detalle de un evento con sesiones incluidas"""
    event = EventService.get_event(db, event_id, include_sessions=True)
    return EventDetailResponse.model_validate(event)


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo evento",
    description="Crea un nuevo evento (requiere rol ORGANIZER)",
)
def create_event(
    event_data: EventCreate,
    current_user: User = Depends(require_roles(UserRole.ORGANIZER)),
    db: Session = Depends(get_db),
):
    """Crear nuevo evento"""
    new_event = EventService.create_event(db, event_data, current_user)
    return EventResponse.model_validate(new_event)


@router.put(
    "/{event_id}",
    response_model=EventResponse,
    summary="Actualizar evento",
    description="Actualiza un evento existente (requiere rol ORGANIZER)",
)
def update_event(
    event_id: int,
    event_data: EventUpdate,
    current_user: User = Depends(require_roles(UserRole.ORGANIZER)),
    db: Session = Depends(get_db),
):
    """Actualizar evento"""
    updated_event = EventService.update_event(db, event_id, event_data, current_user)
    return EventResponse.model_validate(updated_event)


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar evento",
    description="Elimina un evento (requiere rol ORGANIZER)",
)
def delete_event(
    event_id: int,
    current_user: User = Depends(require_roles(UserRole.ORGANIZER)),
    db: Session = Depends(get_db),
):
    """Eliminar evento"""
    EventService.delete_event(db, event_id, current_user)


@router.get(
    "/my/events",
    response_model=EventListResponse,
    summary="Obtener mis eventos",
    description="Obtiene la lista paginada de eventos creados por el usuario actual (requiere rol ORGANIZER o ADMIN)",
)
def get_my_events(
    params: PaginationQueryParams = Depends(),
    current_user: User = Depends(require_roles(UserRole.ORGANIZER)),
    db: Session = Depends(get_db),
):
    """Obtener eventos creados por el usuario actual con paginación (ORGANIZER o ADMIN)"""
    events, pagination_metadata = EventService.get_user_events(
        db, current_user, page=params.page, per_page=params.per_page
    )

    return EventListResponse(
        events=[EventResponse.model_validate(event) for event in events],
        pagination=PaginationMetadata(**pagination_metadata),
    )
