import pytest
from tests.utils import mock_test_data, perform_assertions

from app.tests.utils import PROJECTS_URL, USERS


def test_get_owned_and_collaborated_projects_empty(client, auth_token):
    """Test for getting projects when there are none

    Args:
        client (TestClient):
        auth_token (_type_): _description_
    """
    response = client.get(PROJECTS_URL, headers=auth_token)

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_owned_and_collaborated_projects(client, auth_token):
    mock_project = mock_test_data("project")
    mock_project_2 = mock_test_data("project")

    client.post(PROJECTS_URL, json=mock_project, headers=auth_token)
    client.post(PROJECTS_URL, json=mock_project_2, headers=auth_token)

    response = client.get(PROJECTS_URL, headers=auth_token)

    # Check that the data in the projects has been created correctly
    perform_assertions(
        response,
        http_method="GET",
        mock_projects=[mock_project, mock_project_2],
        len_expected_get=2,
    )


def test_create_project(client, auth_token):
    mock_project = mock_test_data("project")

    response = client.post(PROJECTS_URL, json=mock_project, headers=auth_token)

    perform_assertions(response, http_method="POST", mock_projects=[mock_project])


def test_create_project_with_existing_name(client, auth_token):
    mock_project = mock_test_data("project")

    client.post(PROJECTS_URL, json=mock_project, headers=auth_token)

    # Avoid the description interfering with the test
    mock_project["description"] = "somethingelse"

    # Same name as before
    response = client.post(PROJECTS_URL, json=mock_project, headers=auth_token)

    assert response.status_code == 400
    assert response.json() == {"detail": "User already has a project with that name"}


def test_delete_project(client, auth_token):
    mock_project = mock_test_data("project")

    # This project will have ID 1, since it's the first one created
    client.post(PROJECTS_URL, json=mock_project, headers=auth_token)

    response = client.delete(f"{PROJECTS_URL}/1", headers=auth_token)

    assert response.status_code == 204


def test_delete_project_with_non_existing_id(client, auth_token):
    response = client.delete(f"{PROJECTS_URL}/1", headers=auth_token)

    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}


def test_update_project(client, auth_token):
    mock_project = mock_test_data("project")

    # This project will have ID 1, since it's the first one created
    client.post(PROJECTS_URL, json=mock_project, headers=auth_token)

    # Update project
    mock_project["name"] = "Updated name"
    mock_project["description"] = "Updated description"

    response = client.put(f"{PROJECTS_URL}/1", json=mock_project, headers=auth_token)

    perform_assertions(response, http_method="PUT", mock_projects=[mock_project])


def test_update_project_with_non_existing_id(client, auth_token):
    mock_project = mock_test_data("project")

    # Update project
    mock_project["name"] = "not important"

    response = client.put(f"{PROJECTS_URL}/12324", json=mock_project, headers=auth_token)

    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}
