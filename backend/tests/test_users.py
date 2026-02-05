def test_create_user_as_admin(client, auth_headers_admin):
    """Test creating a user as admin."""
    user_data = {
        "email": "newuser@test.com",
        "password": "password123",
        "full_name": "New User",
        "role": "organizer",
        "is_active": True,
    }

    response = client.post("/api/v1/users/", json=user_data, headers=auth_headers_admin)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["role"] == user_data["role"]


def test_list_users_as_admin(client, auth_headers_admin, test_user_attendee, test_user_organizer):
    """Test listing users as admin."""
    response = client.get("/api/v1/users/", headers=auth_headers_admin)
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert "pagination" in data
    assert len(data["users"]) > 0


def test_get_user_as_admin(client, auth_headers_admin, test_user_attendee):
    """Test getting a user by ID as admin."""
    response = client.get(f"/api/v1/users/{test_user_attendee.id}", headers=auth_headers_admin)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user_attendee.id
    assert data["email"] == test_user_attendee.email


def test_update_user_as_admin(client, auth_headers_admin, test_user_attendee):
    """Test updating a user as admin."""
    update_data = {"full_name": "Updated Name", "is_active": False}

    response = client.put(
        f"/api/v1/users/{test_user_attendee.id}", json=update_data, headers=auth_headers_admin
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == update_data["full_name"]
    assert data["is_active"] == update_data["is_active"]
