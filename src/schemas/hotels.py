from typing import Annotated

from pydantic import BaseModel
from fastapi import Query, Depends



class PaginationHotels(BaseModel):
    page: Annotated[int | None, Query(description="номер страницы")] = 1
    per_page: Annotated[int | None, Query(description="Элементов на странице")] = 5
    
    
class HotelSchema(BaseModel):
    title: str
    location: str
    
class HotelResponceSchema(BaseModel):
    id: int
    title: str
    location: str
    
    class Config:
        from_attributes = True 
    


PiganHotelDep = Annotated[PaginationHotels, Depends()]