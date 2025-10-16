from typing import Annotated

from fastapi import Depends, Request, HTTPException, status, Response
import jwt

from src.service.auth.auth_service import auth_service
from src.utils.db.db_manager import DBManager
from src.core.db.base_model import async_session_maker


def get_token_from_cookie(request: Request):
    access_token = request.cookies.get("access_token", None)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorization"
        )
    return access_token


def valide_delete_token(responce: Response):
    responce.delete_cookie(key="access_token")


LogoutDepen = Annotated[None, Depends(valide_delete_token)]


def get_current_user_id(token: str = Depends(get_token_from_cookie)):
    try:
        user_data: dict = auth_service.decode_token(token=token)

        user_id = user_data.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"detail": "Token is not valid"},
            )
        return user_id
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not valid"
        )


UserIdDepen = Annotated[int, Depends(get_current_user_id)]


async def get_db_manager():
    async with DBManager(session_factory=async_session_maker) as db_manager:
        yield db_manager


DB_Dep = Annotated[DBManager, Depends(get_db_manager)]


