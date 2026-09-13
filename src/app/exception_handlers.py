from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import ConflictError, NotFoundError


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(
        _request: Request,
        exception: NotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exception)},
        )

    @app.exception_handler(ConflictError)
    async def conflict_error_handler(
        _request: Request, exception: ConflictError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exception)},
        )
