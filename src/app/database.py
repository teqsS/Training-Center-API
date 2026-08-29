from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

type SessionFactory = async_sessionmaker[AsyncSession]


def create_engine(database_url: str) -> AsyncEngine:

    async_engine = create_async_engine(
        url=database_url,
        echo=False,
    )

    return async_engine


def create_session_factory(engine: AsyncEngine) -> SessionFactory:

    async_session_factory = async_sessionmaker[AsyncSession](
        bind=engine,
        expire_on_commit=False,
    )

    return async_session_factory
