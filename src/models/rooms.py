from core.db.base_model import Base

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey


class Rooms(Base):
    __tablename__ = "rooms"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]
    