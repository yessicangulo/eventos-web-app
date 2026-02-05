from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import attendees, auth, events, sessions, users
from app.config import settings
from app.core.exceptions import APIException


def create_app() -> FastAPI:
    """Factory function para crear la aplicación FastAPI"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API de Gestión de Eventos - Documentación automática",
        version=settings.VERSION,
        docs_url="/swagger",
        redoc_url="/redoc",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        """Maneja excepciones personalizadas de la API"""
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    app.include_router(
        auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"]
    )
    app.include_router(events.router, prefix=f"{settings.API_V1_PREFIX}/events", tags=["Events"])
    app.include_router(
        sessions.router, prefix=f"{settings.API_V1_PREFIX}/sessions", tags=["Sessions"]
    )
    app.include_router(
        attendees.router, prefix=f"{settings.API_V1_PREFIX}/attendees", tags=["Attendees"]
    )
    app.include_router(users.router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["Users"])

    @app.get("/")
    def root():
        """Endpoint raíz"""
        return {
            "message": "API de Gestión de Eventos",
            "version": settings.VERSION,
            "docs": "Swagger documentation available at /swagger",
        }

    @app.get("/health")
    @app.get(f"{settings.API_V1_PREFIX}/health")
    def health_check():
        """Health check endpoint"""
        return {"status": "healthy"}

    return app
