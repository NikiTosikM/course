from repositories.base_repository import BaseRepository
from models.user import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(session)