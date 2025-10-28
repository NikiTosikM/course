from src.utils.db.db_manager import DBManager


class BaseService():
    def __init__(self, manager: DBManager | None):
        self.manager: DBManager | None = manager