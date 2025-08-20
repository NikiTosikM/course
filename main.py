from fastapi import FastAPI, Body
import uvicorn


app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]

@app.get("/hotels/")
def get_hotels():
    return hotels


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
    hotels[hotel_id-1] = {
        "id": hotel_id,
        "title": title if title else hotels[hotel_id-1]["title"],
        "name": name if name else hotels[hotel_id-1]["name"]
    }
    
    


def main():
    uvicorn.run(
        "main:app",
        reload=True
    )


if __name__ == "__main__":
    main()
