from repositories.base_repository import BaseRepository
from models.user import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session, model, schema = None):
        super().__init__(session, model, schema)