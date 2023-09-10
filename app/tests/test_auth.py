import pytest

from app.tests.utils import (
    AUTH_URL,
    PROJECTS_URL,
    TASKS_URL,
    USERS,
    get_auth_token_second_user,
    mock_test_data,
)


# Authentication
def test_login_for_auth_token(client):
    mock_user = USERS["current_user_create"]

    response = client.post(
        f"{AUTH_URL}/token",
        data={
            "username": mock_user.username,
            "password": mock_user.hashed_password,
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]

    # Check that the token works
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {response.json()['access_token']}"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == mock_user.username
    assert response.json()["email"] == mock_user.email


@pytest.mark.parametrize(
    "username, password",
    [
        ("mock_user.username", "wrongpassword"),  # Wrong username
        ("wrongusername", "mock_user.hashed_password"),  # Wrong password
        ("wrongusername", "wrongpassword"),  # Both wrong
    ],
)
def test_login_for_auth_token_wrong_credentials(client, username, password):
    response = client.post(
        f"{AUTH_URL}/token",
        data={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


# Authorization


def test_update_project_non_authorized(client, auth_token):
    # Get project data
    project_data = mock_test_data("project")

    # This project will have ID 1, since it's the first one created
    client.post(PROJECTS_URL, json=project_data, headers=auth_token)

    # Try to update the task with the second user
    response = client.put(
        url=f"{PROJECTS_URL}/1",
        json=project_data,
        headers=get_auth_token_second_user(client),
    )

    assert response.status_code == 403, f"Response: {response.status_code} -> {response.text}"
    assert response.json() == {"detail": "Not enough permissions"}, response.json()


def test_delete_project_non_authorized(client, auth_token):
    # Get project data
    project_data = mock_test_data("project")

    # This project will have ID 1, since it's the first one created
    client.post(PROJECTS_URL, json=project_data, headers=auth_token)

    # Try to delete the task with the new user
    response = client.delete(
        url=f"{PROJECTS_URL}/1",
        headers=get_auth_token_second_user(client),
    )

    assert response.status_code == 403, f"Response: {response.status_code} -> {response.text}"
    assert response.json() == {"detail": "Not enough permissions"}, response.json()


def test_delete_task_non_authorized(client, auth_token):
    # Get task data
    task_data = mock_test_data("task")

    # This task will have ID 1, since it's the first one created
    client.post(TASKS_URL, json=task_data, headers=auth_token)

    # Try to delete the task with the new user
    response = client.delete(
        url=f"{TASKS_URL}/1",
        headers=get_auth_token_second_user(client),
    )

    assert response.status_code == 403, f"Response: {response.status_code} -> {response.text}"
    assert response.json() == {"detail": "Not enough permissions"}, response.json()


def test_update_task_non_authorized(client, auth_token):
    # Get task data
    task_data = mock_test_data("task")

    # This task will have ID 1, since it's the first one created
    client.post(TASKS_URL, json=task_data, headers=auth_token)

    # Try to delete the task with the new user
    response = client.delete(
        url=f"{TASKS_URL}/1",
        headers=get_auth_token_second_user(client),
    )

    assert response.status_code == 403, f"Response: {response.status_code} -> {response.text}"
    assert response.json() == {"detail": "Not enough permissions"}, response.json()


# This is impossible as is, by the method, and by OAuth protection
# def test_update_my_password_non_authorized(client, auth_token):
#     # Try to update the password of the current user with the second user
#     response = client.patch(
#         url=f"{USERS_URL}/me/password",
#         json={
#             "current_password": USERS["current_user_create"].hashed_password,
#             "new_password": "new_pass",
#         },
#         headers=get_auth_token_second_user(client),
#     )

#     assert response.status_code == 403, f"Response: {response.status_code} -> {response.text}"
#     assert response.json() == {"detail": "Not enough permissions"}, response.json()

# def test_update_my_account_non_authorized(client, auth_token):
#     # Try to update the task with the second user
#     response = client.put(
#         url=f"{USERS_URL}/me/details",
#         json={"username": "new_username1", "email": "new_email@example.com"},
#         headers=get_auth_token_second_user(client),
#     )

#     assert response.status_code == 403, f"Response: {response.status_code} -> {response.text}"
#     assert response.json() == {"detail": "Not enough permissions"}, response.json()
