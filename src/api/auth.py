from fastapi import APIRouter, HTTPException, status

from passlib.context import CryptContext

from schemas.user import UserRequestSchema, UserResponceSchema, UserDBSchema
from models.user import User
from core.db.base_model import async_session_maker
from repositories.user_repository import UserRepository


router = APIRouter(prefix="/auth", tags=["Authenticated and authorization"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.put("/register", response_model=UserResponceSchema)
async def register(user_data: UserRequestSchema):
    hash_password: str = pwd_context.hash(user_data.password)
    user_data_for_db = UserDBSchema(
        name=user_data.name, email=user_data.email, hashpassword=hash_password
    )
    async with async_session_maker() as session:
        availability_user: bool = await UserRepository(
            session=session, model=User
        ).existence_object(email=user_data.email)
        if availability_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": "User is already registered"
                }
            )
        created_user: User = await UserRepository(session=session, model=User).add(
            data=user_data_for_db
        )
        returned_data = UserResponceSchema.model_validate(created_user)
        await session.commit()

    return returned_data
