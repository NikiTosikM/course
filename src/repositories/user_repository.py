from sqlalchemy import Result, select
from fastapi import HTTPException, status

from src.repositories.base_repository import BaseRepository
from src.models.user import User
from src.schemas.user import UserResponceSchema, UserDBSchema


class UserRepository(BaseRepository[User]):
    model = User
    schema = UserResponceSchema
    
    def __init__(self, session):
        super().__init__(session)
        
    async def add_user(self, data: UserDBSchema):
        check_user_query = (
            select(self.model)
            .filter_by(email=data.email)
        )
        result: Result = await self.session.execute(check_user_query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email is already registered"
            )
        
        return await self.add(data=data)