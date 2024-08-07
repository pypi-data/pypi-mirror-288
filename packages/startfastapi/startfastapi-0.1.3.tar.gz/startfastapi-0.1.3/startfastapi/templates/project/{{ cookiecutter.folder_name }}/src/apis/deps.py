import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated, Optional
from pydantic import ValidationError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings
from src.core.db import db_session
from src.apis.user.models import UserModel, UserStatus
from src.apis.user.services import UserService
from src.apis.schema import TokenPayload


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/user/access-token"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]
SessionDep = Annotated[AsyncSession, Depends(db_session)]


async def get_current_user(db: SessionDep, token: TokenDep) -> UserModel:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.SECRET_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    service = UserService(db=db)
    user: Optional[UserModel] = await service.info(id=token_data.sub)
    if not user or user.status == UserStatus.DELETED_USER:
        raise HTTPException(status_code=404, detail="User not found")
    return user

CurrentUserDep = Annotated[UserModel, Depends(get_current_user)]


def get_current_superuser(current_user: CurrentUserDep) -> UserModel:
    if not current_user.status == UserStatus.SUPER_USER:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user

CurrentSuperUserDep = Annotated[UserModel, Depends(get_current_superuser)]