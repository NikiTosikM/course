from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db.base_model import Base


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]
    facilities: Mapped[list["Facilities"]] = relationship(  # noqa: F821
        secondary="room_facilities", back_populates="rooms"
    )

    def __repr__(self):
        return f"{self.__dict__}"
