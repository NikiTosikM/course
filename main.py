from fastapi import FastAPI, Body, Query
import uvicorn


app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"}
]

@app.get("/hotels")
def get_hotels(
    id: int | None = Query(default=None, description='идентификатор отеля'),
    title: str | None = Query(default=None, description="Название нашего отеля"),
    page: int | None = Query(default=1, description="Номер страницы для отображения"),
    per_page : int | None = Query(default=5, description="Количество отображаемых элементов на странице")
):
    hotels_ = []
    for hotel in hotels:
        if title and hotel["title"] != title:
            continue
        if id and hotel["id"] != id:
            continue
        hotels_.append(hotel)
    start, end = (page-1) * per_page, page * per_page
    return hotels_[start: end]
            


@app.put("/hotels/{hotel_id}")
def update_hotel(
    hotel_id: int,
    title: str = Body(),
    name: str = Body()
):
    hotels[hotel_id-1] = {
        "id": hotel_id,
        "title": title,
        "name": name
    }
    
    
@app.patch("/hotels/{hotel_id}")
def change_hotel(
    hotel_id: int,
    title: str | None = Body(default=None),
    name: str | None = Body(default=None),
):
    hotel = hotels[hotel_id-1]
    if title:
        hotel["title"] = title
    elif name:
        hotel["name"] = name
    
    return {"sucess": "ok"}
    
    


def main():
    uvicorn.run(
        "main:app",
        reload=True
    )


if __name__ == "__main__":
    main()
