from src.repositories.base_repository import BaseRepository
from src.models.user import User
from src.schemas.user import UserResponceSchema


class UserRepository(BaseRepository[User]):
    model = User
    schema = UserResponceSchema
    
    def __init__(self, session):
        super().__init__(session)