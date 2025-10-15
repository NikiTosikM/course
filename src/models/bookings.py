from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from src.core.db.base_model import Base


class Booking(Base):
    __tablename__ = "bookings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date] 
    date_to: Mapped[date]
    price: Mapped[int]

    
    
