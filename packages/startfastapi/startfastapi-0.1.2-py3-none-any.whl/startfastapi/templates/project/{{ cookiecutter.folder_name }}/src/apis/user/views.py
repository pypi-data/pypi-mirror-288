from datetime import timedelta
from typing import List, Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.core.config import settings
from src.core.logger import logger
from src.core.security import create_access_token
from src.apis.schema import Token
from src.apis.deps import SessionDep, CurrentUserDep, CurrentSuperUserDep
from src.apis.user.services import UserService
from src.apis.user.schemas import UserCreateSchema, UserInfoSchema, UserUpdateSchema

router = APIRouter(prefix="/users")


@router.post("")
async def create_user(
    db: SessionDep,
    current_user: CurrentSuperUserDep,
    data: UserCreateSchema
):
    logger.info(f"current user = {current_user}")
    service = UserService(db=db)
    result: UserInfoSchema = await service.create(data=data)
    result = UserInfoSchema.from_orm(result)
    return result.model_dump()


@router.delete("/{id}")
async def delete_user(
    db: SessionDep,
    current_user: CurrentSuperUserDep,
    id: str
):
    logger.info(f"current user = {current_user}")
    service = UserService(db=db)
    result: int = await service.delete(id=id)
    return {"count": result}


@router.put("/{id}")
async def update_user(
    db: SessionDep,
    current_user: CurrentUserDep,
    id: str,
    data: UserUpdateSchema
):
    logger.info(f"current user = {current_user}")
    service = UserService(db=db)
    result: int = await service.update(id=id, data=data)
    return {"count": result}


@router.get("/{id}")
async def info_user(
    db: SessionDep,
    current_user: CurrentUserDep,
    id: str
):
    logger.info(f"current user = {current_user}")
    service = UserService(db=db)
    result: UserInfoSchema = await service.info(id=id)
    result = UserInfoSchema.from_orm(result)
    return result.model_dump()


@router.get("")
async def list_user(
    db: SessionDep,
    current_user: CurrentUserDep,
    offset: int = 0,
    limit: int = 10,
    desc: int = 1
):
    logger.info(f"current user = {current_user}")
    service = UserService(db=db)
    result: List[UserInfoSchema] = await service.list(offset=offset, limit=limit, desc=desc)
    result = [UserInfoSchema.from_orm(i).model_dump() for i in result]
    return {"count": len(result), "items": result}


@router.post("/access-token")
async def access_token(
    db: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    service = UserService(db=db)
    user = await service.authenticate(form_data.username, form_data.password)
    if user is None:
        return {}
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(user.id, expires_delta=access_token_expires)
    return Token(access_token=token)
