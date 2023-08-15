from fastapi import APIRouter

from app.api.routes import auth, projects, tasks, users

router = APIRouter()

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(tasks.router)
router.include_router(projects.router)
