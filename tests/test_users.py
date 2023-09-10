"""Tests for the users service."""

from fastapi.testclient import TestClient

from tests.test_utils import USERS, USERS_URL, mock_test_data


def test_create_user(client: TestClient):
    """Nominal test for creating a user.

    Args:
        client (TestClient): Test client
    """
    response = client.post(
        USERS_URL,
        json=mock_test_data("user"),
    )

    assert response.status_code == 201


def test_create_user_with_existing_email(client: TestClient):
    """Test for creating a user with an existing email.

    Args:
        client (TestClient): Test client
    """
    mock_user = mock_test_data("user")

    client.post(
        USERS_URL,
        json=mock_user,
    )

    # Avoid the username interfering with the test
    mock_user["username"] = "SWIM"

    response = client.post(
        USERS_URL,
        json=mock_user,
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_create_user_with_existing_username(client: TestClient):
    """Test for creating a user with an existing username.

    Args:
        client (TestClient): Test client
    """
    mock_user = mock_test_data("user")

    client.post(
        USERS_URL,
        json=mock_user,
    )

    # Avoid the email interfering with the test
    mock_user["email"] = "somethingelse@example.com"

    # Same username as beforez
    response = client.post(
        USERS_URL,
        json=mock_user,
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}


def test_read_my_user(client: TestClient, auth_token: dict) -> None:
    """Nominal test for getting the current user.

    Args:
        client (TestClient): Test client
        auth_token (fixture): JWT token for authentication
    """
    mock_user = USERS["current_user_create"]

    response = client.get(
        f"{USERS_URL}/me",
        headers=auth_token,
    )

    assert response.status_code == 200
    assert response.json()["username"] == mock_user.username
    assert response.json()["email"] == mock_user.email


def test_update_account_password(client: TestClient, auth_token: dict) -> None:
    """Nominal test for updating the current user's password.

    Args:
        client (TestClient): Test client
        auth_token (fixture): JWT token for authentication
    """
    mock_user = USERS["current_user_create"]

    response = client.patch(
        f"{USERS_URL}/me/password",
        headers=auth_token,
        json={
            "current_password": mock_user.hashed_password,
            "new_password": "NewPassword1!",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"detail": "Password updated successfully"}

    # Check that the new password works
    response = client.post(
        "/api/auth/token",
        data={
            "username": mock_user.username,
            "password": "NewPassword1!",
        },
    )

    assert response.status_code == 200


def test_update_account_password_short_password(client: TestClient, auth_token: dict) -> None:
    """Test for updating the current user's password with a password that is too short.

    Args:
        client (TestClient): Test client
        auth_token (fixture): JWT token for authentication
    """
    mock_user = USERS["current_user_create"]

    response = client.patch(
        f"{USERS_URL}/me/password",
        headers=auth_token,
        json={
            "current_password": mock_user.hashed_password,
            "new_password": "!AbCd1",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Password must be at least 8 characters long"}


def test_update_account_password_no_regex_match(client: TestClient, auth_token: dict) -> None:
    """Test for updating the current user's password with a password that does not match the regex.

    Args:
        client (TestClient): Test client
        auth_token (fixture): JWT token for authentication
    """
    mock_user = USERS["current_user_create"]

    response = client.patch(
        f"{USERS_URL}/me/password",
        headers=auth_token,
        json={
            "current_password": mock_user.hashed_password,
            "new_password": "passwordddddd",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Password must contain at least one number, one lowercase and one uppercase letter, and at least one special character"
    }


def test_update_account_details(client: TestClient, auth_token: dict) -> None:
    """Nominal test for updating the current user's details.

    Args:
        client (TestClient): Test client
        auth_token (fixture): JWT token for authentication
    """
    mock_user = USERS["current_user_create"]

    new_username = "newusername"

    response = client.put(
        f"{USERS_URL}/me/details",
        headers=auth_token,
        json={
            "email": mock_user.email,  # Keep it as is
            "username": new_username,
        },
    )

    assert response.status_code == 200
    assert response.json()["username"] == new_username
    assert response.json()["email"] == mock_user.email

    # Check that the new username works

    response = client.post(
        "/api/auth/token",
        data={
            "username": new_username,
            "password": mock_user.hashed_password,
        },
    )

    assert response.status_code == 200


def test_delete_my_account(client: TestClient, auth_token: dict) -> None:
    """Nominal test for deleting the current user.

    Args:
        client (TestClient): Test client
        auth_token (fixture): JWT token for authentication
    """
    response = client.delete(
        f"{USERS_URL}/me",
        headers=auth_token,
    )

    assert response.status_code == 204

    # Check that the user is actually deleted
    response = client.get(
        f"{USERS_URL}/me",
        headers=auth_token,
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
