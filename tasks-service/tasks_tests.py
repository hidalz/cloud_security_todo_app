"""Tests for tasks service."""

from fastapi.testclient import TestClient

from app.tests.utils import PROJECTS_URL, TASKS_URL, mock_test_data, perform_assertions


def test_get_own_tasks(client: TestClient, auth_token: dict) -> None:
    """Test for getting tasks when there are none.

    Args:
        client (TestClient):
        auth_token (fixture): JWT token for authentication
    """
    # Empty tasks
    response = client.get(TASKS_URL, headers=auth_token)

    perform_assertions(response, "GET", len_expected_get=0)

    # Get tasks when there are several
    mock_task = mock_test_data("task")
    client.post(
        TASKS_URL,
        json=mock_task,
        headers=auth_token,
    )

    response = client.get(TASKS_URL, headers=auth_token)

    perform_assertions(response, "GET", len_expected_get=1)


def test_create_own_task(client: TestClient, auth_token: dict) -> None:
    """Nominal test for creating a task.

    Args:
        client (TestClient): Test client
        auth_token (fixture): JWT token for authentication
    """
    mock_task = mock_test_data("task")

    response = client.post(
        TASKS_URL,
        json=mock_task,
        headers=auth_token,
    )

    perform_assertions(response, "POST", mock_task, owner_id=1, parent_id=None, project_id=None)


def test_create_own_task_with_parent(client: TestClient, auth_token: dict) -> None:
    """Nominal test for creating a task with a parent task.

    Args:
        client (TestClient): Test client
        auth_token (fixture): JWT token for authentication
    """
    mock_task_parent = mock_test_data("task")
    mock_task_child = mock_test_data("task", parent_id=1)

    # Parent task will have id 1 in DB
    client.post(
        TASKS_URL,
        json=mock_task_parent,
        headers=auth_token,
    )

    response = client.post(
        TASKS_URL,
        json=mock_task_child,
        headers=auth_token,
    )

    perform_assertions(
        response, "POST", mock_task_child, owner_id=1, parent_id=1, project_id=None
    )


def test_create_own_task_with_project(client: TestClient, auth_token: dict) -> None:
    """Nominal test for creating a task with a project.

    Args:
        client (TestClient): Test client
        auth_token (fixture): JWT token for authentication
    """
    mock_project = mock_test_data("project")

    # Create project. This will have id 1 in DB, since it is the first project created
    project_response = client.post(
        PROJECTS_URL,
        json=mock_project,
        headers=auth_token,
    )
    perform_assertions(project_response, "POST", mock_projects=[mock_project])

    mock_task = mock_test_data("task", project_id=1)

    task_response = client.post(
        TASKS_URL,
        json=mock_task,
        headers=auth_token,
    )

    perform_assertions(task_response, "POST", mock_task, owner_id=1, parent_id=None, project_id=1)


def test_update_task(client: TestClient, auth_token: dict) -> None:
    """Nominal test for updating a task.

    Args:
        client (TestClient): Test client
        auth_token (fixture): JWT token for authentication
    """
    mock_task = mock_test_data("task")

    # Create task. This will have id 1 in DB, since it is the first task created
    client.post(
        TASKS_URL,
        json=mock_task,
        headers=auth_token,
    )

    # Update task
    mock_task["title"] = "Updated title"
    mock_task["description"] = "Updated description"
    mock_task["priority"] = 2

    response = client.put(
        f"{TASKS_URL}/1",
        json=mock_task,
        headers=auth_token,
    )

    perform_assertions(response, "PUT", mock_task, owner_id=1, parent_id=None, project_id=None)


def test_delete_task(client: TestClient, auth_token: dict) -> None:
    """Nominal test for deleting a task.

    Args:
        client (TestClient): Test client
        auth_token (fixture): JWT token for authentication
    """
    mock_task = mock_test_data("task")

    # Create task. This will have id 1 in DB, since it is the first task created
    client.post(
        TASKS_URL,
        json=mock_task,
        headers=auth_token,
    )

    # Delete task
    response = client.delete(
        f"{TASKS_URL}/1",
        headers=auth_token,
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Task 1 deleted"}

    # Check what happens when deleting a non-existing task
    response = client.delete(
        f"{TASKS_URL}/1",
        headers=auth_token,
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
