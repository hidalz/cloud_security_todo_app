from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes.api import router as api_router

from . import settings

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "https://localhost:8080",
]


def get_application() -> FastAPI:
    application = FastAPI(**settings.FASTAPI_KWARGS)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix=settings.API_PREFIX)

    return application


app = get_application()
