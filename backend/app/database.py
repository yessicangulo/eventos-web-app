from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency para obtener la sesión de BD en FastAPI.
    Usa yield pattern para cerrar automáticamente la sesión al final del request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
