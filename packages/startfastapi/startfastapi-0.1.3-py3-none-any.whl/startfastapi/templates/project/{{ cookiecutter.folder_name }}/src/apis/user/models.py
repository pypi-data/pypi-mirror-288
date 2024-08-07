from enum import Enum
from typing import Optional
from sqlmodel import Field
from src.apis.model import Base


class UserStatus(Enum):
    SUPER_USER: int = 1 << 0
    NORMAL_USER: int = 1 << 1
    DELETED_USER: int = 1 << 2


class UserModel(Base, table=True):
    """
    User Model
    """

    __tablename__ = "user"

    username: str = Field(nullable=False, unique=True, index=True, min_length=1, max_length=32)
    password: str = Field(nullable=False, unique=False)
    status: Optional[UserStatus] = Field(default=UserStatus.NORMAL_USER, nullable=True, unique=False)
