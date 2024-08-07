from typing import Optional
from pydantic import Field, BaseModel
from src.apis.schema import BaseSchema, BaseInfoSchema


class UserCreateSchema(BaseSchema):

    username: str = Field(min_length=1, max_length=32)
    password: str = Field()


class UserInfoSchema(UserCreateSchema, BaseInfoSchema):
    status: int


class UserUpdateSchema(BaseModel):

    username: Optional[str] = Field(default=None, min_length=1, max_length=32)
    password: Optional[str] = Field(default=None)
    status: Optional[int] = Field(default=1)

