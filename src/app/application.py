from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import Settings
from app.database import create_engine, create_session_factory
from app.routers import (
    courses_router,
    enrollments_router,
    statistics_router,
    students_router,
    system_router,
)


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine = create_engine(app_settings.DATABASE_URL_asyncpg)
        session_factory = create_session_factory(engine)

        app.state.engine = engine
        app.state.session_factory = session_factory

        try:
            yield
        finally:
            await engine.dispose()

    app = FastAPI(
        lifespan=lifespan,
        title="training_center_api",
        version="0.1.0",
    )

    app.include_router(system_router, prefix="/training_center_api")
    app.include_router(courses_router, prefix="/training_center_api")
    app.include_router(students_router, prefix="/training_center_api")
    app.include_router(enrollments_router, prefix="/training_center_api")
    app.include_router(statistics_router, prefix="/training_center_api")

    return app
