from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.apis.service import BaseService
from src.apis.{{ cookiecutter.folder_name }}.models import {{ cookiecutter.class_name }}Model
from src.apis.{{ cookiecutter.folder_name }}.schemas import {{ cookiecutter.class_name }}CreateSchema, {{ cookiecutter.class_name }}InfoSchema, {{ cookiecutter.class_name }}UpdateSchema


class {{ cookiecutter.class_name }}Service(BaseService[{{ cookiecutter.class_name }}Model, {{ cookiecutter.class_name }}CreateSchema, {{ cookiecutter.class_name }}UpdateSchema, {{ cookiecutter.class_name }}InfoSchema]):

    def __init__(self, db: AsyncSession):
        super().__init__(model={{ cookiecutter.class_name }}Model, db=db)

