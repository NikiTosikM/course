from typing import Annotated

from pydantic import BaseModel, ConfigDict
from fastapi import Query, Depends



class PaginationHotels(BaseModel):
    page: Annotated[int | None, Query(description="номер страницы")] = 1
    per_page: Annotated[int | None, Query(description="Элементов на странице")] = 5
    
    
class HotelSchema(BaseModel):
    title: str
    location: str
    
class HotelPartialUpdateSchema(BaseModel):
    title: str | None = None
    location: str | None = None
    
class HotelResponceSchema(BaseModel):
    id: int
    title: str
    location: str
    
    model_config = ConfigDict(
        from_attributes=True)
    


PiganHotelDep = Annotated[PaginationHotels, Depends()]