from typing import Annotated

from pydantic import BaseModel
from fastapi import Query, Depends



class PaginationHotels(BaseModel):
    page: Annotated[int | None, Query(description="номер страницы")] = 1
    per_page: Annotated[int | None, Query(description="Элементов на странице")] = 5
    


PiganHotelDep = Annotated[PaginationHotels, Depends()]