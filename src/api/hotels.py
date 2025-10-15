from typing import Annotated
from datetime import date

from fastapi import APIRouter, Query
from src.api.dependencies import DB_Dep
from schemas.hotels import (
    HotelSchema,
    HotelResponceSchema,
    HotelPartialUpdateSchema,
    PiganHotelDep
)


router = APIRouter(tags=["Работа с отелями"])


@router.get("/hotels")
async def get_hotels(
    db_manager: DB_Dep,
    pig_hotels: PiganHotelDep,
    data_from: Annotated[date, Query(description="Дата заезда")] = "2025-09-10",
    date_to: Annotated[date, Query(description="Дата выезда")] = "2025-09-15",
    location: Annotated[str | None, Query(description="Локация")] = None,
    title: Annotated[str | None, Query(description="Название отеля")] = None
):
    hotels = await db_manager.hotel.get_filtered(
            date_to=date_to,
            date_from=data_from,
            location=location,
            title=title,
            pig_hotels=pig_hotels
        )

    return hotels

@router.post("/hotels")
async def create_hotel(db_manager: DB_Dep, hotel_data: HotelSchema) -> dict:
        hotel: HotelResponceSchema = await db_manager.hotel.add(data=hotel_data)
        await db_manager.commit()

        return {"status": "OK", "data": hotel}


@router.put("/hotels/{hotel_id}")
async def update_hotel(db_manager: DB_Dep, hotel_id: int, hotel_data: HotelSchema):
    db_manager.hotel.update(
            data=hotel_data, id=hotel_id
        )
    await db_manager.commit()
    


@router.delete("/hotels/{hotel_id}")
async def delete_hotel(db_manager: DB_Dep, hotel_id: int):
    db_manager.hotel.delete(id=hotel_id)
    await db_manager.commit()

    return {"status": "ok"}


@router.patch("/hotels/{hotel_id}")
async def change_hotel(db_manager: DB_Dep, hotel_id: int, hotel_data: HotelPartialUpdateSchema):
    db_manager.hotel.update(
            exclude_unset=True, data=hotel_data, id=hotel_id
        )
    await db_manager.commit()

    return {"status": "ok"}


@router.get("/{hotel_id}")
async def get_hotel(db_manager: DB_Dep, hotel_id: int):
    hotel = await db_manager.hotel.specific_object(
            hotel_id=hotel_id
        )
    await db_manager.commit()

    return {"status": "ok", "hotel": hotel}
