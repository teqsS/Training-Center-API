from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import async_engine
from app.routers import (
    courses_router,
    enrollments_router,
    statistics_router,
    students_router,
    system_router,
)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    yield
    await async_engine.dispose()


def create_app() -> FastAPI:

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


app = create_app()
