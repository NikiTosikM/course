from typing import Annotated
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


from fastapi import FastAPI, Body, Query
import uvicorn

from schemas.hotels import PiganHotelDep


app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@app.get("/hotels")
def get_hotels(
    pig_hotels: PiganHotelDep,
    id: Annotated[int | None, Query(description="идентификатор отеля")] = None,
    title: Annotated[str | None, Query(description="Название отеля")] = None,
):
    hotels_ = []
    for hotel in hotels:
        if title and hotel["title"] != title:
            continue
        if id and hotel["id"] != id:
            continue
        hotels_.append(hotel)
    start, end = (
        (pig_hotels.page - 1) * pig_hotels.per_page,
        pig_hotels.page * pig_hotels.per_page,
    )
    return hotels_[start:end]


@app.put("/hotels/{hotel_id}")
def update_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    hotels[hotel_id - 1] = {"id": hotel_id, "title": title, "name": name}


@app.patch("/hotels/{hotel_id}")
def change_hotel(
    hotel_id: int,
    title: str | None = Body(default=None),
    name: str | None = Body(default=None),
):
    hotel = hotels[hotel_id - 1]
    if title:
        hotel["title"] = title
    elif name:
        hotel["name"] = name

    return {"sucess": "ok"}


def main():
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    main()
