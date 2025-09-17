from fastapi import APIRouter, HTTPException, status, Response

from schemas.user import (
    UserRequestSchema,
    UserResponceSchema,
    UserDBSchema,
    UserLoginSchema,
)
from models.user import User
from core.db.base_model import async_session_maker
from repositories.user_repository import UserRepository
from service.auth.auth_service import auth_service
from api.dependencies import UserIdDepen, LogoutDepen


router = APIRouter(prefix="/auth", tags=["Authenticated and authorization"])


@router.post("/register", response_model=UserResponceSchema)
async def register(user_data: UserRequestSchema):
    hash_password: str = auth_service.create_hastpassword(password=user_data.password)
    user_data_for_db = UserDBSchema(
        name=user_data.name, email=user_data.email, hashpassword=hash_password
    )
    async with async_session_maker() as session:
        created_user: User = await UserRepository(session=session, model=User).add(
            data=user_data_for_db
        )
        returned_data = UserResponceSchema.model_validate(created_user)
        await session.commit()

    return returned_data


@router.post("/login")
async def login(login_data: UserLoginSchema, responce: Response):
    async with async_session_maker() as session:
        user: User | None = await UserRepository(
            session=session, model=User
        ).get_one_or_none(email=login_data.email)
        await session.commit()
    verify_hashpassword: bool = auth_service.verify_password(
        password=login_data.password, hashpassword=user.hashpassword
    ) if user else None
    if not user or not verify_hashpassword:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Account login details are incorrect"},
        )
        
    access_token: str =auth_service.create_access_token(user_id=user.id)
    responce.set_cookie(key="access_token", value=access_token)
        
    return {"access_token": access_token}


@router.get("/me")
async def about_me(user_id: UserIdDepen): # type: ignore
    async with async_session_maker() as session:
        user = await UserRepository(session=session, model=User).get_one_or_none(id=user_id)
        await session.commit()
    
    return user

@router.post("/logout")
async def logout(token: LogoutDepen):
    return {"status": "ok"}