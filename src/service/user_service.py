from fastapi import Response
from src.exceptions.exceptions import UserLoginIncorrect
from src.service.base_service import BaseService

from src.schemas.user import UserRequestSchema
from src.service.auth.auth_service import AuthService
from src.schemas.user import UserResponceSchema, UserDBSchema
from src.models.user import User
from src.schemas.user import (
    UserLoginSchema,
)


class UserService(BaseService):
    async def register_user(self, user_data: UserRequestSchema):
        hash_password: str = AuthService().create_hastpassword(
            password=user_data.password
        )
        user_data_for_db = UserDBSchema(
            name=user_data.name, email=user_data.email, hashpassword=hash_password
        )
        created_user: UserResponceSchema = await self.manager.user.add_user(
            data=user_data_for_db
        )
        await self.session.commit()

        return created_user

    async def login(self, login_data: UserLoginSchema, responce: Response):
        user: User | None = await self.manager.user.get_user(
            email=login_data.email
        )
            
        verify_hashpassword: bool = (
            AuthService().verify_password(
                password=login_data.password, hashpassword=user.hashpassword
            )
            if user
            else None
        )
        if not user or not verify_hashpassword:
            raise UserLoginIncorrect()
        
        access_token: str = AuthService().create_access_token(user_id=user.id)
        responce.set_cookie(key="access_token", value=access_token)

        return {"access_token": access_token}
