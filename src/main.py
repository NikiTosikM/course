from typing import Annotated


from fastapi import FastAPI, Query
import uvicorn
from sqlalchemy import select, Result
from models.hotels import Hotels

from schemas.hotels import PiganHotelDep
from core.db.base_model import async_session_maker


app = FastAPI()


@app.get("/hotels")
async def get_hotels(
    pig_hotels: PiganHotelDep,
    location: Annotated[str | None, Query(description="город где находится отель")] = None,
    title: Annotated[str | None, Query(description="Название отеля")] = None,
):
    query = select(Hotels)
    if title:
        query = query.where(Hotels.title.like(f"%{title}%"))
    if location:
        query = query.where(Hotels.location.like(f"%{location}%"))
    query = (
        query
        .limit(pig_hotels.per_page)
        .offset((pig_hotels.page-1) * pig_hotels.per_page)
    )
    async with async_session_maker() as session:
        result: Result =  await session.execute(query)
        
    return result.scalars().all()


# @app.put("/hotels/{hotel_id}")
# def update_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
#     hotels[hotel_id - 1] = {"id": hotel_id, "title": title, "name": name}


# @app.patch("/hotels/{hotel_id}")
# def change_hotel(
#     hotel_id: int,
#     title: str | None = Body(default=None),
#     name: str | None = Body(default=None),
# ):
#     hotel = hotels[hotel_id - 1]
#     if title:
#         hotel["title"] = title
#     elif name:
#         hotel["name"] = name

#     return {"sucess": "ok"}


def main():
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    main()
