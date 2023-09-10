from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from common_components.application.api_router import api_router
from common_components.database import settings

# Provide a list of origins that should be permitted to make cross-origin requests (CORS).
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "https://localhost:8080",
]


def get_application() -> FastAPI:
    """Get application.

    Returns:
        FastAPI: FastAPI application.
    """
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
