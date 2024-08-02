from datetime import datetime
from pydantic import BaseModel, Field


class BaseSchema(BaseModel):

    class Config:
        from_attributes = True


class BaseInfoSchema(BaseSchema):

    id: str = Field()
    created_at: datetime = Field(default=datetime.now)
    updated_at: datetime = Field(default=datetime.now)

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        data["created_at"] = data["created_at"].strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        data["updated_at"] = data["updated_at"].strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return data


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenPayload(BaseModel):
    sub: str | None = None