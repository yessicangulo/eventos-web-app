def test_create_event(client, test_user_organizer, auth_headers_organizer, test_event_data):
    """Test creating an event."""
    response = client.post("/api/v1/events/", json=test_event_data, headers=auth_headers_organizer)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_event_data["name"]


def test_list_events(client, test_user_organizer, auth_headers_organizer, test_event_data):
    """Test listing events."""
    client.post("/api/v1/events/", json=test_event_data, headers=auth_headers_organizer)
    response = client.get("/api/v1/events/")
    assert response.status_code == 200
    data = response.json()
    assert "events" in data or isinstance(data, list)


def test_get_event_by_id(client, test_user_organizer, auth_headers_organizer, test_event_data):
    """Test getting event by ID."""
    create_response = client.post(
        "/api/v1/events/", json=test_event_data, headers=auth_headers_organizer
    )
    event_id = create_response.json()["id"]
    response = client.get(f"/api/v1/events/{event_id}")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data or data.get("id") == event_id


def test_update_event(client, test_user_organizer, auth_headers_organizer, test_event_data):
    """Test updating an event."""
    create_response = client.post(
        "/api/v1/events/", json=test_event_data, headers=auth_headers_organizer
    )
    event_id = create_response.json()["id"]
    update_data = {"name": "Updated Event Name"}
    response = client.put(
        f"/api/v1/events/{event_id}", json=update_data, headers=auth_headers_organizer
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Event Name"


def test_delete_event(client, test_user_organizer, auth_headers_organizer, test_event_data):
    """Test deleting an event."""
    create_response = client.post(
        "/api/v1/events/", json=test_event_data, headers=auth_headers_organizer
    )
    event_id = create_response.json()["id"]
    response = client.delete(f"/api/v1/events/{event_id}", headers=auth_headers_organizer)
    assert response.status_code == 204
    get_response = client.get(f"/api/v1/events/{event_id}")
    assert get_response.status_code == 404


def test_get_my_events(client, test_user_organizer, auth_headers_organizer, test_event_data):
    """Test getting my events."""
    client.post("/api/v1/events/", json=test_event_data, headers=auth_headers_organizer)
    response = client.get("/api/v1/events/my/events", headers=auth_headers_organizer)
    assert response.status_code == 200
    data = response.json()
    assert "events" in data
    assert len(data["events"]) > 0
