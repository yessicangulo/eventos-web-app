from datetime import timedelta

import pytest


@pytest.fixture
def test_session_data(test_event_data):
    """Test session data."""
    from datetime import datetime, timedelta

    start = datetime.utcnow() + timedelta(days=1, hours=1)
    end = start + timedelta(hours=2)
    return {
        "event_id": 1,
        "title": "Test Session",
        "description": "Test Session Description",
        "speaker_name": "Test Speaker",
        "speaker_bio": "Test Speaker Bio",
        "start_time": start.isoformat(),
        "end_time": end.isoformat(),
        "location": "Test Location",
        "capacity": 50,
    }


@pytest.fixture
def test_event_for_session(db, test_user_organizer, test_event_data):
    """Create a test event for session tests."""
    from app.crud import event as crud_event
    from app.schemas.event import EventCreate

    event = crud_event.create_event(
        db=db, event=EventCreate(**test_event_data), creator_id=test_user_organizer.id
    )
    db.refresh(event)
    return event


def test_get_session(
    client, test_event_for_session, test_user_organizer, auth_headers_organizer, test_session_data
):
    """Test getting a session by ID."""
    session_data = test_session_data.copy()
    session_data["event_id"] = test_event_for_session.id
    event_start = test_event_for_session.start_date
    session_data["start_time"] = (event_start + timedelta(hours=1)).isoformat()
    session_data["end_time"] = (event_start + timedelta(hours=3)).isoformat()

    create_response = client.post(
        "/api/v1/sessions/", json=session_data, headers=auth_headers_organizer
    )
    session_id = create_response.json()["id"]
    response = client.get(f"/api/v1/sessions/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == session_id
    assert data["title"] == session_data["title"]


def test_create_session(client, test_event_for_session, auth_headers_organizer, test_session_data):
    """Test creating a session."""
    session_data = test_session_data.copy()
    session_data["event_id"] = test_event_for_session.id
    event_start = test_event_for_session.start_date
    session_data["start_time"] = (event_start + timedelta(hours=1)).isoformat()
    session_data["end_time"] = (event_start + timedelta(hours=3)).isoformat()

    response = client.post("/api/v1/sessions/", json=session_data, headers=auth_headers_organizer)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == session_data["title"]
    assert data["event_id"] == test_event_for_session.id


def test_update_session(client, test_event_for_session, auth_headers_organizer, test_session_data):
    """Test updating a session."""
    session_data = test_session_data.copy()
    session_data["event_id"] = test_event_for_session.id
    event_start = test_event_for_session.start_date
    session_data["start_time"] = (event_start + timedelta(hours=1)).isoformat()
    session_data["end_time"] = (event_start + timedelta(hours=3)).isoformat()

    create_response = client.post(
        "/api/v1/sessions/", json=session_data, headers=auth_headers_organizer
    )
    session_id = create_response.json()["id"]
    update_data = {"title": "Updated Session Title"}
    response = client.put(
        f"/api/v1/sessions/{session_id}", json=update_data, headers=auth_headers_organizer
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Session Title"


def test_delete_session(client, test_event_for_session, auth_headers_organizer, test_session_data):
    """Test deleting a session."""
    session_data = test_session_data.copy()
    session_data["event_id"] = test_event_for_session.id
    event_start = test_event_for_session.start_date
    session_data["start_time"] = (event_start + timedelta(hours=1)).isoformat()
    session_data["end_time"] = (event_start + timedelta(hours=3)).isoformat()

    create_response = client.post(
        "/api/v1/sessions/", json=session_data, headers=auth_headers_organizer
    )
    session_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/sessions/{session_id}", headers=auth_headers_organizer)
    assert response.status_code == 204

    get_response = client.get(f"/api/v1/sessions/{session_id}")
    assert get_response.status_code == 404
