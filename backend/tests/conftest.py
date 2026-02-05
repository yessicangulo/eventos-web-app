import os
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import create_app
from app.core.security import create_access_token, get_password_hash
from app.database import Base, get_db
from app.models.user import User, UserRole

# Base de datos de prueba en memoria
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db():
    """Create a database session for tests."""
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client for the app."""
    app = create_app()

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Test user data."""
    return {"email": "test@example.com", "password": "testpassword123", "full_name": "Test User"}


@pytest.fixture
def test_event_data():
    """Test event data."""
    from datetime import datetime, timedelta

    return {
        "name": "Test Event",
        "description": "Test Description",
        "location": "Test Location",
        "start_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "end_date": (datetime.utcnow() + timedelta(days=2)).isoformat(),
        "capacity": 100,
    }


@pytest.fixture
def test_user_attendee(db):
    """Create a test user with ATTENDEE role."""
    user = User(
        email="attendee@test.com",
        hashed_password=get_password_hash("testpass123"),
        full_name="Test Attendee",
        role=UserRole.ATTENDEE,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_user_organizer(db):
    """Create a test user with ORGANIZER role."""
    user = User(
        email="organizer@test.com",
        hashed_password=get_password_hash("testpass123"),
        full_name="Test Organizer",
        role=UserRole.ORGANIZER,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_user_admin(db):
    """Create a test user with ADMIN role."""
    user = User(
        email="admin@test.com",
        hashed_password=get_password_hash("testpass123"),
        full_name="Test Admin",
        role=UserRole.ADMIN,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers_attendee(test_user_attendee):
    """Get auth headers for attendee user."""
    access_token = create_access_token(
        data={"sub": test_user_attendee.email}, expires_delta=timedelta(minutes=30)
    )
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def auth_headers_organizer(test_user_organizer):
    """Get auth headers for organizer user."""
    access_token = create_access_token(
        data={"sub": test_user_organizer.email}, expires_delta=timedelta(minutes=30)
    )
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def auth_headers_admin(test_user_admin):
    """Get auth headers for admin user."""
    access_token = create_access_token(
        data={"sub": test_user_admin.email}, expires_delta=timedelta(minutes=30)
    )
    return {"Authorization": f"Bearer {access_token}"}
