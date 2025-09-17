from typing import Annotated

from fastapi import Depends, Request, HTTPException, status, Response
import jwt

from service.auth.auth_service import auth_service


def get_token_from_cookie(request: Request):
    access_token = request.cookies.get("access_token", None)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorization"
        )
    return access_token


def valide_delete_token(responce: Response, token: str = Depends(get_token_from_cookie)):
    try:
        user_data: dict = auth_service.decode_token(token=token)
        responce.delete_cookie(key="access_token")
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not valid"
        )
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature has expired"
        )


def get_current_user_id(token: str = Depends(get_token_from_cookie)):
    try:
        user_data: dict = auth_service.decode_token(token=token)
        
        user_id = user_data.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "detail": "Token is not valid"
                }
            )
        return user_id
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not valid"
        )

UserIdDepen =  Annotated[int, Depends(get_current_user_id)]
LogoutDepen = Annotated[None, Depends(valide_delete_token)]