"""Test utilities. This module contains common functions and variables used in the tests."""

from faker import Faker
from fastapi.testclient import TestClient
from requests import Response

from app.schemas.users import UserInDB

USERS = {
    "current_user_create": UserInDB(
        username="user1",
        email="user1@example.com",
        hashed_password="Password1!",
    ),
    "second_user_create": UserInDB(
        username="user2",
        email="user2@example.com",
        hashed_password="Password2!",
    ),
}

# API Routes
USERS_URL = "/api/users"
TASKS_URL = "/api/tasks"
PROJECTS_URL = "/api/projects"
AUTH_URL = "api/auth"


def mock_test_data(
    item: str, parent_id: int | None = None, project_id: int | None = None
) -> dict:
    """Mock test data.

    Args:
        item (str): Item to mock.

    Returns:
        dict: Mocked data.
    """
    fake = Faker()

    mock_data_mapping = {
        "user": {
            "username": fake.name(),
            "email": fake.email(),
            "hashed_password": fake.password(
                length=9,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ),
        },
        "task": {
            "title": fake.name(),
            "description": fake.text(),
            "priority": 1,
            "parent_id": parent_id,
            "project_id": project_id,
        },
        "project": {
            "name": fake.name(),
            "description": fake.text(),
        },
    }

    return mock_data_mapping.get(item, {})  # Returns an empty dictionary if item is not found


def perform_assertions(
    response: Response,
    http_method: str,
    mock_task: dict | None = None,
    mock_projects: list | None = None,
    len_expected_get: int | None = None,
    owner_id: int | None = None,
    parent_id: int | None = None,
    project_id: int | None = None,
) -> None:
    """Perform task assertions.

    It asserts the response against the data inputted. It checks task content, relationships and
    the expected response status code and type of the API.

    Args:
        response (): _description_
        mock_task (_type_): _description_
        http_method (_type_): _description_
        owner_id (int | None, optional): _description_. Defaults to None.
        parent_id (int | None, optional): _description_. Defaults to None.
        project_id (int | None, optional): _description_. Defaults to None.
    """
    # Response assertions (http_method)
    if http_method == "POST":
        assert response.status_code == 201, f"Response: {response.status_code} -> {response.text}"
        assert isinstance(response.json(), dict), "Response should be a JSON object"
    elif http_method == "GET":
        assert response.status_code == 200, f"Response: {response.status_code} -> {response.text}"
        assert isinstance(response.json(), list), "Response should be a JSON list"
        assert len(response.json()) == len_expected_get, f"Received {len(response.json())}"
    elif http_method == "PUT":
        assert response.status_code == 200, f"Response: {response.status_code} -> {response.text}"
        assert isinstance(response.json(), dict), "Response should be a JSON object"
    # Task content assertions (mock_task)
    if mock_task:
        assert response.json()["title"] == mock_task.get("title")
        assert response.json()["description"] == mock_task.get("description")
        assert response.json()["priority"] == mock_task.get("priority")

    if mock_projects:
        for counter, project in enumerate(mock_projects):
            assert project["name"] == mock_projects[counter].get("name")
            assert project["description"] == mock_projects[counter].get("description")

    # Task relationship assertions (owner_id, parent_id, project_id)
    if owner_id:
        assert response.json()["owner_id"] == owner_id
    if parent_id:
        assert response.json()["parent_id"] == parent_id
    if project_id:
        assert response.json()["project_id"] == project_id


def get_auth_token_second_user(client: TestClient) -> dict:
    """Get auth token for second user.

    Args:
        client (TestClient): Test client.

    Returns:
        dict: Auth token.
    """
    # Login with the second user (already in DB from the fixtures)
    response = client.post(
        f"{AUTH_URL}/token",
        data={
            "username": USERS["second_user_create"].username,
            "password": USERS["second_user_create"].hashed_password,
        },
    )
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
