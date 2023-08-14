from fastapi import APIRouter

from app.api.routes import authentication, projects, tasks, users

router = APIRouter()

# router.include_router(authentication.router, tags=["authentication"], prefix="/users")
router.include_router(users.router)
router.include_router(tasks.router)
router.include_router(projects.router)
