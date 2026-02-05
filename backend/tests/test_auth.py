def test_register_user(client, test_user_data):
    """Test user registration."""
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert "password" not in data


def test_register_duplicate_email(client, test_user_data):
    """Test registration with duplicate email."""
    client.post("/api/v1/auth/register", json=test_user_data)
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 400
    assert "ya está registrado" in response.json()["detail"].lower()


def test_login_success(client, test_user_data):
    """Test successful login."""
    client.post("/api/v1/auth/register", json=test_user_data)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": test_user_data["email"], "password": test_user_data["password"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user_data):
    """Test login with wrong password."""
    client.post("/api/v1/auth/register", json=test_user_data)
    response = client.post(
        "/api/v1/auth/login", json={"email": test_user_data["email"], "password": "wrongpassword"}
    )
    assert response.status_code in [400, 401]


def test_get_current_user(client, test_user_data):
    """Test getting current user."""
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": test_user_data["email"], "password": test_user_data["password"]},
    )
    token = login_response.json()["access_token"]
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]


def test_get_current_user_no_token(client):
    """Test getting current user without token."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code in [401, 403]
