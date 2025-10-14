from repositories.base_repository import BaseRepository
from models.user import User
from schemas.user import UserResponceSchema


class UserRepository(BaseRepository[User]):
    model = User
    schema = UserResponceSchema
    
    def __init__(self, session):
        super().__init__(session)