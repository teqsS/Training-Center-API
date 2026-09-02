from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application import create_app
from app.config import Settings


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


@pytest.fixture
def app(settings: Settings) -> FastAPI:

    app = create_app(settings)

    return app


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:

    with TestClient(app) as client:
        yield client
