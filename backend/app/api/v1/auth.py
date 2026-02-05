from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.core.deps import get_current_user
from app.core.security import create_access_token
from app.crud import attendee as crud_attendee
from app.crud import event as crud_event
from app.database import get_db
from app.models.user import User
from app.schemas.event import EventResponse
from app.schemas.user import Token, UserCreate, UserLogin, UserProfileResponse, UserResponse
from app.services.user_service import UserService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea un nuevo usuario en el sistema. Los usuarios registrados desde este endpoint siempre se crean con rol 'attendee' (asistente).",
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registrar nuevo usuario (siempre como asistente/attendee)"""
    new_user = UserService.register_user(db, user_data)
    return UserResponse.model_validate(new_user)


@router.post(
    "/login",
    response_model=Token,
    summary="Login de usuario",
    description="Autentica un usuario y retorna un token JWT",
)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login de usuario"""
    user = UserService.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/me",
    response_model=UserProfileResponse,
    summary="Obtener perfil del usuario actual",
    description="Retorna el perfil completo del usuario autenticado con eventos registrados",
)
def read_users_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Obtener perfil completo del usuario actual"""
    registered_events = crud_attendee.get_user_registered_events_all(db, user_id=current_user.id)
    created_events = crud_event.get_user_events_all(db, user_id=current_user.id)
    created_events_count = len(created_events)

    registered_events_response = [
        EventResponse.model_validate(event) for event in registered_events
    ]

    user_base = UserResponse.model_validate(current_user)
    profile_response = UserProfileResponse(
        **user_base.model_dump(),
        registered_events=registered_events_response,
        created_events_count=created_events_count,
    )

    return profile_response
