from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey

from core.db.base_model import Base


class Booking(Base):
    __tablename__ = "bookings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date] 
    date_to: Mapped[date]
    price: Mapped[int]
    
    def __init__(self, date_from: date, date_to: date, price: int):
        self.date_from = date_from
        self.date_to = date_to
        self.price = price
    
    @hybrid_property
    def total_price(self):
        return self.price * (self.date_to - self.date_from).days
    
    
