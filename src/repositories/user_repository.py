from sqlalchemy import Result, select

from src.repositories.base_repository import BaseRepository
from src.models.user import User
from src.schemas.user import UserResponceSchema, UserDBSchema
from src.exceptions.exceptions import UserAlreadyCreatedError


class UserRepository(BaseRepository[User]):
    model = User
    schema = UserResponceSchema

    def __init__(self, session):
        super().__init__(session)

    async def add_user(self, data: UserDBSchema):
        check_user_query = select(self.model).filter_by(email=data.email)
        result: Result = await self.session.execute(check_user_query)
        if result.scalar_one_or_none():
            raise UserAlreadyCreatedError(email=data.email)

        return await self.add(data=data)
