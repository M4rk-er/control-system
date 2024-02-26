from typing import (Annotated, Any, AsyncGenerator, Dict, List, Sequence,
                    TypeVar)

from sqlalchemy import Delete, Insert, Select, String, Update
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.pool import NullPool

from src.config.db_settings import settings

async_engine = create_async_engine(
    url=settings.DB_URL,
    # echo=True,
)

if settings.MODE == 'TEST':
    async_engine = create_async_engine(
        url=settings.TEST_URL,
        poolclass=NullPool,
    )

async_session = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine
)


class Base(DeclarativeBase):

    repr_cols_num = 5
    repr_cols = tuple()

    def __repr__(self) -> str:
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def fetch_one(query: Select | Insert | Update) -> Any | None:
    async with async_session() as conn:
        result = await conn.execute(query)
        return result.unique().scalar_one_or_none()


async def fetch_all(query: Select | Insert | Update) -> Sequence[Any]:
    async with async_session() as conn:
        result = await conn.execute(query)
        return result.scalars().unique().all()


async def execute(
    query: Insert | Update | Delete,
    values: Dict | List | None = None,
):
    async with async_session() as conn:
        res = await conn.execute(query, values)
        try:
            obj = res.scalar_one_or_none()
            await conn.commit()
            return obj
        except ResourceClosedError:
            await conn.commit()
            return


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str128 = Annotated[str, mapped_column(String(128))]

ModelType = TypeVar('ModelType', bound=Base)
