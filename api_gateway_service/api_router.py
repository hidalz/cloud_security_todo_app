from fastapi import APIRouter

from auth_service.auth_router import router as auth_router
from projects_service.projects_router import router as project_router
from tasks_service.tasks_router import router as task_router
from users_service.users_router import router as user_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(task_router)
api_router.include_router(project_router)
