from collections.abc import AsyncIterator, Iterator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from app.application import create_app
from app.config import Settings
from app.database import create_engine


@pytest.fixture
def settings() -> Settings:
    settings = Settings(
        _env_file=None,
        DB_USER="postgres",
        DB_PASS="secret",
        DB_HOST="localhost",
        DB_PORT=5432,
        DB_NAME="postgres_db",
    )

    return settings


@pytest.fixture(scope="session")
def database_settings() -> Settings:
    settings = Settings(
        _env_file=None,
    )

    if not settings.DB_NAME.startswith("test_"):
        raise RuntimeError("The name of the test database should start with 'test_'")

    return settings


@pytest_asyncio.fixture(scope="function")
async def database_engine(database_settings: Settings) -> AsyncIterator[AsyncEngine]:
    engine = create_engine(
        database_url=database_settings.DATABASE_URL_asyncpg,
    )

    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def clean_database(database_engine: AsyncEngine) -> AsyncIterator[None]:

    async def truncate_tables() -> None:

        stmt = text("""
            TRUNCATE TABLE
            courses,
            students,
            enrollments
            RESTART IDENTITY CASCADE;
        """)

        async with database_engine.begin() as connection:
            await connection.execute(stmt)

    await truncate_tables()

    try:
        yield
    finally:
        await truncate_tables()


@pytest.fixture
def app(settings: Settings) -> FastAPI:

    app = create_app(settings)

    return app


@pytest.fixture(scope="function")
def database_app(database_settings: Settings) -> FastAPI:

    app = create_app(database_settings)

    return app


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def database_client(
    database_app: FastAPI, clean_database: None
) -> Iterator[TestClient]:

    with TestClient(database_app) as client:
        yield client
