import os

import httpx  # A Python HTTP client for making requests to other services
from fastapi import APIRouter
from starlette.requests import Request

from auth_service.auth_router import router as auth_router
from projects_service.projects_router import router as project_router
from tasks_service.tasks_router import router as task_router
from users_service.users_router import router as user_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(task_router)
api_router.include_router(project_router)

# Define the microservices and their default host/port values
microservices = {"auth": "8001", "projects": "8002", "tasks": "8003", "users": "8004"}

# Read environment variables and build URLs using a dictionary comprehension
service_urls = {
    service: f"http://{os.environ.get(f'{service.upper()}_SERVICE_HOST', f'{service}-service')}:{os.environ.get(f'{service.upper()}_SERVICE_PORT', default_port)}/{service}"
    for service, default_port in microservices.items()
}


# Route to the Authentication Microservice
@api_router.post("/auth/{endpoint}", response_model=str)
async def route_to_auth_service(endpoint: str, request: Request):
    # Build the URL for the auth service endpoint
    url = f"{service_urls['auth']}/{endpoint}"

    # Forward the request to the auth service
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method, url, headers=dict(request.headers), json=await request.json()
        )

    return response.text


# Route to the Projects Microservice
@api_router.post("/projects/{endpoint}", response_model=str)
async def route_to_projects_service(endpoint: str, request: Request):
    # Build the URL for the projects service endpoint
    url = f"{service_urls['projects']}/{endpoint}"

    # Forward the request to the projects service
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method, url, headers=dict(request.headers), json=await request.json()
        )

    return response.text


# Route to the Tasks Microservice
@api_router.post("/tasks/{endpoint}", response_model=str)
async def route_to_tasks_service(endpoint: str, request: Request):
    # Build the URL for the tasks service endpoint
    url = f"{service_urls['tasks']}/{endpoint}"

    # Forward the request to the tasks service
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method, url, headers=dict(request.headers), json=await request.json()
        )

    return response.text


# Route to the Users Microservice
@api_router.post("/users/{endpoint}", response_model=str)
async def route_to_users_service(endpoint: str, request: Request):
    # Build the URL for the users service endpoint
    url = f"{service_urls['users']}/{endpoint}"

    # Forward the request to the users service
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method, url, headers=dict(request.headers), json=await request.json()
        )

    return response.text
