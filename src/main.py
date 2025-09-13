from typing import Annotated


from fastapi import FastAPI, Query, Body
import uvicorn
from models.hotels import Hotels

from core.db.base_model import async_session_maker
from models.hotels import Hotels
from repositories.hotel_repository import HoterRepository
from schemas.hotels import HotelSchema, PiganHotelDep, HotelResponceSchema


app = FastAPI()


@app.get("/hotels")
async def get_hotels(
    pig_hotels: PiganHotelDep,
    location: Annotated[
        str | None, Query(description="город где находится отель")
    ] = None,
    title: Annotated[str | None, Query(description="Название отеля")] = None,
):
    async with async_session_maker() as session:
        hotels: list[Hotels] = await HoterRepository(
            model=HoterRepository, session=session
        ).get_all(
            location=location,
            title=title,
            page=pig_hotels.page,
            per_page=pig_hotels.per_page,
        )

    return hotels


@app.post("/hotels")
async def create_hotel(hotel_data: HotelSchema) -> dict:
    async with async_session_maker() as session:
        hotel_model: Hotels = await HoterRepository(session=session, model=Hotels).add(
            data=hotel_data
        )
        await session.commit()
        
    hotel = HotelResponceSchema.model_validate(hotel_model)

    return {"status": "OK", "data": hotel}


@app.put("/hotels/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelSchema):
    async with async_session_maker() as session:
        await HoterRepository(session=session, model=Hotels).update(
            data=hotel_data,
            id=hotel_id
        )
        await session.commit()
        
        
@app.delete("/hotels/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HoterRepository(session=session, model=Hotels).delete(
            id=hotel_id
        )
        await session.commit()


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
