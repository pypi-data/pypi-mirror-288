from typing import (
    Optional,
    List,
    TypeVar,
    Type,
    Generic
)
from pydantic import BaseModel
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.apis.model import ModelType


CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel, covariant=True)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel, covariant=True)
InfoSchemaType = TypeVar("InfoSchemaType", bound=BaseModel, covariant=True)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType, InfoSchemaType]):
    """
    Base Service
    """
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def create(self, data: CreateSchemaType) -> InfoSchemaType:
        """
        Create API
        """

        # 创建时，不需要设置 exclude_unset=True。
        record = self.model(**data.model_dump())
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record

    async def delete(self, id: str) -> int:
        """
        Delete API
        """

        record = await self.db.execute(delete(self.model).where(self.model.id == id))
        await self.db.commit()
        return record.rowcount

    async def delete_all(self) -> int:
        """
        Delete All API
        """

        record = await self.db.execute(delete(self.model))
        await self.db.commit()
        return record.rowcount

    async def update(self, id: str, *, data: UpdateSchemaType) -> int:
        """
        Update API
        """

        record = await self.db.execute(
            update(self.model).where(self.model.id == id).values(**data.model_dump(exclude_unset=True))  # 更新时，只更新设置的内容。
        )
        await self.db.commit()
        return record.rowcount

    async def info(self, id: str) -> Optional[InfoSchemaType]:
        """
        Info API
        """

        record = await self.db.execute(select(self.model).where(self.model.id == id))
        return record.scalars().first()

    async def list(self, offset: int, limit: int, desc: int) -> List[InfoSchemaType]:
        """
        List API
        """

        record = select(self.model).offset(offset).limit(limit)

        if desc == 1:
            record = record.order_by(self.model.updated_at.desc())
        else:
            record = record.order_by(self.model.updated_at)
        record = await self.db.execute(record)

        return record.scalars().all()

    async def total(self) -> int:
        """
        Total API
        """

        record = await self.db.execute(select(func.count(self.model.id)))
        return record.scalars().first()
