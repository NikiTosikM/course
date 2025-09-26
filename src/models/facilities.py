from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from core.db.base_model import Base


class Facilities(Base):
    __tablename__ = "facilities"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    

class RoomFacilities(Base):
    __tablename__ = "room_facilities"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
    
    