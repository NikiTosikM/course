from fastapi import APIRouter, Response

from src.schemas.user import (
    UserRequestSchema,
    UserResponceSchema,
    UserLoginSchema,
)
from src.api.dependencies import UserIdDepen, LogoutDepen
from src.api.dependencies import DB_Dep
from src.exceptions.exceptions import (
    UserAlreadyCreatedError,
    UserEmailAlreadyRegisterHTTPException,
    UserLoginIncorrect,
    UserLoginIncorrectHTTPException,
    UserNotFoundHTTPException,
    UserNotFoundError
)
from src.service.user_service import UserService


router = APIRouter(prefix="/auth", tags=["Authenticated and authorization"])


@router.post("/register", response_model=UserResponceSchema)
async def register(user_data: UserRequestSchema, db: DB_Dep):
    try:
        created_user = await UserService(db).register_user(user_data=user_data)

        return created_user
    except UserAlreadyCreatedError:
        raise UserEmailAlreadyRegisterHTTPException


@router.post("/login")
async def login(login_data: UserLoginSchema, responce: Response, db: DB_Dep):
   try:
       access_token = await UserService(db).login(login_data, responce)
       
       return {"access_token": access_token}
   except UserLoginIncorrect:
       raise UserLoginIncorrectHTTPException


@router.get("/me")
async def about_me(user_id: UserIdDepen, db: DB_Dep):  # type: ignore
    try:
        user = await db.user.get_one_or_none(id=user_id)

        return user
    except UserNotFoundError:
        raise UserNotFoundHTTPException


@router.post("/logout")
async def logout(token: LogoutDepen):
    return {"status": "ok"}
