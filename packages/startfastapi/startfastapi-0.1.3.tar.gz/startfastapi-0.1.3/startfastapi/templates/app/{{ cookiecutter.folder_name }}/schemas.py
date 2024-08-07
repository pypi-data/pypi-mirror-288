from typing import Optional
from pydantic import Field, BaseModel
from src.apis.schema import BaseSchema, BaseInfoSchema


class {{ cookiecutter.class_name }}CreateSchema(BaseSchema):
    ...


class {{ cookiecutter.class_name }}InfoSchema({{ cookiecutter.class_name }}CreateSchema, BaseInfoSchema):
    ...


class {{ cookiecutter.class_name }}UpdateSchema(BaseModel):
    ...