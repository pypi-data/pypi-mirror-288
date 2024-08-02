#!/usr/bin/env python3
from typing import Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.base import MappedBase

ModelType = TypeVar('ModelType', bound=MappedBase)


class CRUDModelBase:
    """Base class for CRUD operations on a model.

    Parameters
    ----------
    model : Type[ModelType]
        The SQLAlchemy model type.
    """

    async def create_(self, db: AsyncSession, create_data: ModelType) -> ModelType:
        """Create a new record in the database.

        :param db: AsyncSession
        :param create_data:  Model class
        :return:
        """
        db.add(create_data)
        await db.flush()
        return create_data


BaseDao: CRUDModelBase = CRUDModelBase()
