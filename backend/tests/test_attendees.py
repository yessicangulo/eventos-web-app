import pytest


@pytest.fixture
def test_event_for_attendee(db, test_user_organizer, test_event_data):
    """Create a test event for attendee tests."""
    from app.crud import event as crud_event
    from app.schemas.event import EventCreate

    event = crud_event.create_event(
        db=db, event=EventCreate(**test_event_data), creator_id=test_user_organizer.id
    )
    db.refresh(event)
    return event


def test_register_to_event(client, test_event_for_attendee, auth_headers_attendee):
    """Test registering to an event."""
    response = client.post(
        f"/api/v1/attendees/register/{test_event_for_attendee.id}", headers=auth_headers_attendee
    )
    assert response.status_code == 201
    data = response.json()
    assert "message" in data
    assert data["data"]["event_id"] == test_event_for_attendee.id


def test_unregister_from_event(client, test_event_for_attendee, auth_headers_attendee):
    """Test unregistering from an event."""
    client.post(
        f"/api/v1/attendees/register/{test_event_for_attendee.id}", headers=auth_headers_attendee
    )
    response = client.delete(
        f"/api/v1/attendees/unregister/{test_event_for_attendee.id}", headers=auth_headers_attendee
    )
    assert response.status_code == 204


def test_get_my_registered_events(client, test_event_for_attendee, auth_headers_attendee):
    """Test getting my registered events."""
    client.post(
        f"/api/v1/attendees/register/{test_event_for_attendee.id}", headers=auth_headers_attendee
    )
    response = client.get("/api/v1/attendees/my-events", headers=auth_headers_attendee)
    assert response.status_code == 200
    data = response.json()
    assert "events" in data
    assert "pagination" in data
    assert len(data["events"]) > 0


def test_get_event_attendees(
    client, test_event_for_attendee, auth_headers_organizer, auth_headers_attendee
):
    """Test getting event attendees as organizer."""
    client.post(
        f"/api/v1/attendees/register/{test_event_for_attendee.id}", headers=auth_headers_attendee
    )
    response = client.get(
        f"/api/v1/attendees/event/{test_event_for_attendee.id}/attendees",
        headers=auth_headers_organizer,
    )
    assert response.status_code == 200
    data = response.json()
    assert "event_id" in data
    assert "total_attendees" in data
    assert "attendees" in data
    assert len(data["attendees"]) > 0


def test_check_registration_true(client, test_event_for_attendee, auth_headers_attendee):
    """Test checking registration when registered."""
    client.post(
        f"/api/v1/attendees/register/{test_event_for_attendee.id}", headers=auth_headers_attendee
    )
    response = client.get(
        f"/api/v1/attendees/check/{test_event_for_attendee.id}", headers=auth_headers_attendee
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_registered"] is True
