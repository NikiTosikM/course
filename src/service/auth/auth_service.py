from datetime import datetime, timezone, timedelta

from passlib.context import CryptContext
from core.config import settings
import jwt


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, password: str, hashpassword: str) -> bool:
        return self.pwd_context.verify(password, hashpassword)

    def create_hastpassword(self, password: str):
        return self.pwd_context.hash(password)

    def create_access_token(self, user_id: int):
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.token.access_token_expire_minutes
        )
        data = {"user_id": user_id, "exp": int(expire.timestamp())}
        encoded_jwt = jwt.encode(
            data, settings.token.secret_key, algorithm=settings.token.algorithm
        )
        
        return encoded_jwt


auth_service = AuthService()