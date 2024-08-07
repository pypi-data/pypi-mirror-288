from uuid import uuid4
from datetime import datetime
from typing import Optional, TypeVar
from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declared_attr
from sqlalchemy.dialects.mysql import DATETIME
from sqlmodel import Field, SQLModel


class Base(SQLModel):
    """
    Base Model
    """

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True,
        nullable=False
    )

    created_at: Optional[datetime] = Field(sa_type=DATETIME(fsp=6), default_factory=datetime.now)
    # updated_at: Optional[datetime] = Field(sa_type=DATETIME(fsp=6), onupdate=datetime.now, default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(sa_column=Column(DATETIME(fsp=6), default=datetime.now, onupdate=datetime.now))


ModelType = TypeVar("ModelType", bound=Base)

