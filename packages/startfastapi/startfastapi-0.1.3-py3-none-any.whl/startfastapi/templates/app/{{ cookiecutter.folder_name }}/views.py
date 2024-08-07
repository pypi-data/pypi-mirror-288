from datetime import timedelta
from typing import List, Annotated
from fastapi import APIRouter, Depends
from src.core.config import settings
from src.core.logger import logger
from src.apis.deps import SessionDep, CurrentUserDep, CurrentSuperUserDep
from src.apis.{{ cookiecutter.folder_name }}.services import {{ cookiecutter.class_name }}Service
from src.apis.{{ cookiecutter.folder_name }}.schemas import {{ cookiecutter.class_name }}CreateSchema, {{ cookiecutter.class_name }}InfoSchema, {{ cookiecutter.class_name }}UpdateSchema

router = APIRouter(prefix="/{{ cookiecutter.folder_name }}s")


@router.post("")
async def create_{{ cookiecutter.folder_name }}(
    db: SessionDep,
    current_user: CurrentSuperUserDep,
    data: {{ cookiecutter.class_name }}CreateSchema
):
    service = {{ cookiecutter.class_name }}Service(db=db)
    result: {{ cookiecutter.class_name }}InfoSchema = await service.create(data=data)
    result = {{ cookiecutter.class_name }}InfoSchema.from_orm(result)
    return result.model_dump()


@router.delete("/{id}")
async def delete_{{ cookiecutter.folder_name }}(
    db: SessionDep,
    current_user: CurrentSuperUserDep,
    id: str
):
    service = {{ cookiecutter.class_name }}Service(db=db)
    result: int = await service.delete(id=id)
    return {"count": result}


@router.put("/{id}")
async def update_{{ cookiecutter.folder_name }}(
    db: SessionDep,
    current_user: CurrentUserDep,
    id: str,
    data: {{ cookiecutter.class_name }}UpdateSchema
):
    service = {{ cookiecutter.class_name }}Service(db=db)
    result: int = await service.update(id=id, data=data)
    return {"count": result}


@router.get("/{id}")
async def info_{{ cookiecutter.folder_name }}(
    db: SessionDep,
    current_user: CurrentUserDep,
    id: str
):
    service = {{ cookiecutter.class_name }}Service(db=db)
    result: {{ cookiecutter.class_name }}InfoSchema = await service.info(id=id)
    result = {{ cookiecutter.class_name }}InfoSchema.from_orm(result)
    return result.model_dump()


@router.get("")
async def list_{{ cookiecutter.folder_name }}(
    db: SessionDep,
    current_user: CurrentUserDep,
    offset: int = 0,
    limit: int = 10,
    desc: int = 1
):
    service = {{ cookiecutter.class_name }}Service(db=db)
    result: List[{{ cookiecutter.class_name }}InfoSchema] = await service.list(offset=offset, limit=limit, desc=desc)
    result = [{{ cookiecutter.class_name }}InfoSchema.from_orm(i).model_dump() for i in result]
    return {"count": len(result), "items": result}