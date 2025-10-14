from sqlalchemy.orm import Mapped, mapped_column

from src.core.db.base_model import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashpassword: Mapped[str]