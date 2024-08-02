from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.apis.service import BaseService
from src.apis.user.models import UserModel
from src.apis.user.schemas import UserCreateSchema, UserInfoSchema, UserUpdateSchema


class UserService(BaseService[UserModel, UserCreateSchema, UserUpdateSchema, UserInfoSchema]):

    def __init__(self, db: AsyncSession):
        super().__init__(model=UserModel, db=db)

    async def info_by_name(self, username: str) -> UserModel:
        """
        Info By Name API
        """

        record = await self.db.execute(select(self.model).where(self.model.username == username))
        return record.scalars().first()

    async def authenticate(self, username: str, password: str) -> UserModel:
        user = await self.info_by_name(username)
        if not user:
            return None
        if user.password != password:
            return None
        return user
