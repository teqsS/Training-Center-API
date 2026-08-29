import asyncio

import uvicorn
from fastapi import FastAPI

from app.routers import (
    courses_router,
    enrollments_router,
    statistics_router,
    students_router,
    system_router,
)

app = FastAPI(
    title="training_center_api",
    version="0.1.0",
)
app.include_router(system_router, prefix="/training_center_api")
app.include_router(courses_router, prefix="/training_center_api")
app.include_router(students_router, prefix="/training_center_api")
app.include_router(enrollments_router, prefix="/training_center_api")
app.include_router(statistics_router, prefix="/training_center_api")


async def main():
    uvicorn.run(
        app="main:app",
        reload=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
