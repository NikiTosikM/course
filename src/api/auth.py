from fastapi import APIRouter, HTTPException, status, Response

from src.schemas.user import (
    UserRequestSchema,
    UserResponceSchema,
    UserDBSchema,
    UserLoginSchema,
)
from src.models.user import User
from src.service.auth.auth_service import auth_service
from src.api.dependencies import UserIdDepen, LogoutDepen
from src.api.dependencies import DB_Dep
from src.exceptions.exceptions import UserAlreadyCreatedError


router = APIRouter(prefix="/auth", tags=["Authenticated and authorization"])


@router.post("/register", response_model=UserResponceSchema)
async def register(user_data: UserRequestSchema, db: DB_Dep):
    hash_password: str = auth_service.create_hastpassword(password=user_data.password)
    user_data_for_db = UserDBSchema(
        name=user_data.name, email=user_data.email, hashpassword=hash_password
    )
    try:
        created_user: UserResponceSchema = await db.user.add_user(data=user_data_for_db)
        await db.commit()

        return created_user
    except UserAlreadyCreatedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email is already registered",
        )


@router.post("/login")
async def login(login_data: UserLoginSchema, responce: Response, db: DB_Dep):
    user: User | None = await db.user.get_one_or_none(email=login_data.email)
    verify_hashpassword: bool = (
        auth_service.verify_password(
            password=login_data.password, hashpassword=user.hashpassword
        )
        if user
        else None
    )
    if not user or not verify_hashpassword:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Account login details are incorrect"},
        )

    access_token: str = auth_service.create_access_token(user_id=user.id)
    responce.set_cookie(key="access_token", value=access_token)

    return {"access_token": access_token}


@router.get("/me")
async def about_me(user_id: UserIdDepen, db: DB_Dep):  # type: ignore
    user = await db.user.get_one_or_none(id=user_id)

    return user


@router.post("/logout")
async def logout(token: LogoutDepen):
    return {"status": "ok"}
