from collections.abc import AsyncGenerator
from typing import Annotated, cast

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionFactory


async def get_session(request: Request) -> AsyncGenerator[AsyncSession]:
    session_factory = cast(
        SessionFactory,
        request.app.state.session_factory,
    )

    async with session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


SessionDep = Annotated[
    AsyncSession,
    Depends(get_session),
]
