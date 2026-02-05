from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.pagination import PaginationMetadata, PaginationQueryParams
from app.schemas.session import SessionCreate, SessionListResponse, SessionResponse, SessionUpdate
from app.services.session_service import SessionService

router = APIRouter()


@router.get(
    "/event/{event_id}",
    response_model=SessionListResponse,
    summary="Obtener sesiones de un evento",
    description="Obtiene la lista paginada de sesiones de un evento específico",
)
def get_event_sessions(
    event_id: int, params: PaginationQueryParams = Depends(), db: Session = Depends(get_db)
):
    """Obtener sesiones de un evento con paginación"""
    sessions, pagination_metadata = SessionService.get_event_sessions(
        db, event_id, page=params.page, per_page=params.per_page
    )
    return SessionListResponse(
        sessions=[SessionResponse.model_validate(session) for session in sessions],
        pagination=PaginationMetadata(**pagination_metadata),
    )


@router.get(
    "/{session_id}",
    response_model=SessionResponse,
    summary="Obtener detalle de sesión",
    description="Obtiene el detalle de una sesión específica",
)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """Obtener detalle de una sesión"""
    session = SessionService.get_session(db, session_id)
    return SessionResponse.model_validate(session)


@router.post(
    "/",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva sesión",
    description="Crea una nueva sesión para un evento (requiere rol ORGANIZER)",
)
def create_session(
    session_data: SessionCreate,
    current_user: User = Depends(require_roles(UserRole.ORGANIZER)),
    db: Session = Depends(get_db),
):
    """Crear nueva sesión"""
    new_session = SessionService.create_session(db, session_data, current_user)
    return SessionResponse.model_validate(new_session)


@router.put(
    "/{session_id}",
    response_model=SessionResponse,
    summary="Actualizar sesión",
    description="Actualiza una sesión existente (requiere rol ORGANIZER)",
)
def update_session(
    session_id: int,
    session_data: SessionUpdate,
    current_user: User = Depends(require_roles(UserRole.ORGANIZER)),
    db: Session = Depends(get_db),
):
    """Actualizar sesión"""
    updated_session = SessionService.update_session(db, session_id, session_data)
    return SessionResponse.model_validate(updated_session)


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar sesión",
    description="Elimina una sesión (requiere rol ORGANIZER)",
)
def delete_session(
    session_id: int,
    current_user: User = Depends(require_roles(UserRole.ORGANIZER)),
    db: Session = Depends(get_db),
):
    """Eliminar sesión"""
    SessionService.delete_session(db, session_id)
