from typing import Generic, Sequence, TypeVar

from fastapi import HTTPException, status
from pydantic import BaseModel

from src.config.database import ModelType
from src.data.base import CrudBase
from src.exceptions import DoesNotExistDB, DuplicateDb

CrudType = TypeVar('CrudType', bound=CrudBase)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
FilterSchemaType = TypeVar('FilterSchemaType', bound=BaseModel)


class BaseService(Generic[ModelType, CrudType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, orm_model: CrudType) -> None:
        self.orm_model = orm_model

    async def list_objs(
        self, offset: int, limit: int, **filters
    ) -> Sequence[ModelType]:

        return await self.orm_model.select_all(offset, limit, filters)

    async def get_obj(self, obj_id: int | None, **filters) -> ModelType | None:

        try:
            if obj_id:
                filters = {'id': obj_id, **filters}
            return await self.orm_model.select_by(**filters)

        except DoesNotExistDB:
            obj_name = self.orm_model.model.__name__
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail=f'There are no {obj_name}.'
            )

    async def create_obj(self, data: CreateSchemaType) -> ModelType | None:

        try:
            formated_data = data.model_dump()
            obj_id = await self.orm_model.insert(formated_data)
            obj = await self.get_obj(obj_id=obj_id)
            return obj

        except DuplicateDb:
            obj_name = self.orm_model.model.__name__
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'This {obj_name} already exists.',
            )

    async def update_obj(
        self, obj_id: int, new_values: UpdateSchemaType
    ) -> ModelType | None:

        await self.orm_model.update(obj_id, new_values)
        obj = await self.get_obj(obj_id=obj_id)
        return obj

    async def partial_update_obj(
        self, obj_id: int, new_values: UpdateSchemaType
    ) -> ModelType | None:

        data = new_values.model_dump(exclude_unset=True)
        await self.orm_model.update(obj_id, data)
        obj = await self.get_obj(obj_id)
        return obj

    async def delete_obj(self, obj_id: int) -> None:

        try:
            await self.orm_model.delete(obj_id)
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

        except DoesNotExistDB:
            obj_name = self.orm_model.model.__name__
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f'There are no {obj_name} with this id.',
            )
