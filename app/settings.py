import os

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "todo_app")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "This Is A Password!1%_")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_NAME = os.getenv("DATABASE_NAME", "todo_app")
DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

FASTAPI_KWARGS = {
    "title": "TODO App",
    "description": "A TODO app built with FastAPI and PostgreSQL for my Master's thesis in Cybersecurity",
    "version": "0.0.1",
    "terms_of_service": "https://example.com/terms/",
    "contact": {
        "name": "Moisés Hidalgo",
        "url": "https://linkedin.com/in/moiseshidalgo/",
    },
    "license_info": {"name": "MIT", "url": "https://mit-license.org/"},
}

API_PREFIX = "/api"
