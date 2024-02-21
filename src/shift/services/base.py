from typing import Generic, Sequence, TypeVar

from fastapi import HTTPException, status
from pydantic import BaseModel

from src.database import Base
from src.shift.data.base import CrudBase
from src.shift.exceptions import DoesNotExistDB, DuplicateDb

ModelType = TypeVar('ModelType', bound=Base)
CrudType = TypeVar('CrudType', bound=CrudBase)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseService(Generic[ModelType, CrudType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, orm_model: CrudType) -> None:
        self.orm_model = orm_model

    async def list(self) -> Sequence[ModelType]:
        return await self.orm_model.select_all()

    async def get_obj(self, obj_id: int | None) -> ModelType | None:

        try:
            return await self.orm_model.select_by(id=obj_id)

        except DoesNotExistDB:
            obj_name = self.orm_model.model.__name__
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f'There are no {obj_name} with this id.'
            )

    async def create_obj(self, data: CreateSchemaType) -> ModelType | None:

        try:
            obj_id = await self.orm_model.insert(data)
            obj = await self.get_obj(obj_id=obj_id)
            return obj

        except DuplicateDb:
            obj_name = self.orm_model.model.__name__
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'This {obj_name} already exists.'
            )

    async def update_obj(self, obj_id: int, new_values: UpdateSchemaType) -> ModelType | None:

        await self.orm_model.update(obj_id, new_values)
        obj = await self.get_obj(obj_id=obj_id)
        return obj

    async def delete_obj(self, obj_id: int) -> None:

        try:
            await self.orm_model.delete(obj_id)
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

        except DoesNotExistDB:
            obj_name = self.orm_model.model.__name__
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f'There are no {obj_name} with this id.'
            )
