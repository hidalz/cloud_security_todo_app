import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app import settings
from app.db.database import Base, get_db
from app.main import app
from app.services.users import create_user
from app.tests.utils import USERS

### DB ###

# Create the DB engine object and the DB Session
engine = create_engine(settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set up the database once
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture()
def session():
    """Get a DB session for a test case.

    It creates a transaction, recreates it when the application code calls session.commit
    and rolls it back at the end.

    https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites

    Yields:
        TestingSessionLocal: A SQLAlchemy session object.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()

    transaction.rollback()
    # Reset the sequences
    session.execute(text("SELECT setval('tasks_id_seq', 1, false);"))
    session.execute(text("SELECT setval('users_id_seq', 1, false);"))
    session.execute(text("SELECT setval('projects_id_seq', 1, false);"))
    connection.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        return session

    # Create the two test users in the DB itself
    create_user(session, USERS["current_user_create"])
    create_user(session, USERS["second_user_create"])

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    del app.dependency_overrides[get_db]


@pytest.fixture()
def auth_token(client):
    response = client.post(
        "/api/auth/token",
        data={
            "username": USERS["current_user_create"].username,
            "password": USERS["current_user_create"].hashed_password,
        },
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
