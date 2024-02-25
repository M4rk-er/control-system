from typing import Generic, Optional, Sequence, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from src.config.database import Base, execute, fetch_all, fetch_one
from src.exceptions import DoesNotExistDB, DuplicateDb

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def select_all(
        self, offset: Optional[int], limit: Optional[int], filters
    ) -> Sequence[ModelType]:

        query = (
            select(self.model)
            .filter_by(**filters)
            .order_by('id')
            .offset(offset)
            .limit(limit)
        )
        result = await fetch_all(query)

        return result

    async def select_by(self, **filters) -> ModelType:

        query = select(self.model).filter_by(**filters)
        result = await fetch_one(query)

        if not result:
            raise DoesNotExistDB

        return result

    async def insert(self, obj_in: dict) -> ModelType | None:

        try:
            stmt = insert(self.model).values(obj_in).returning(self.model.id)
            obj_id = await execute(stmt)
            return obj_id

        except IntegrityError:
            raise DuplicateDb

    async def update(self, pk: int, obj_in: UpdateSchemaType | dict) -> int | None:

        stmt = (
            update(self.model)
            .where(self.model.id == pk)
            .values(**obj_in)
            .returning(self.model.id)
        )

        obj_id = await execute(stmt)
        return obj_id

    async def delete(self, pk: int) -> None:

        is_exists = select(self.model).filter_by(id=pk)
        exists = await fetch_one(is_exists)

        if exists:
            stmt = delete(self.model).where(self.model.id == pk)
            await execute(stmt)
            return

        raise DoesNotExistDB
