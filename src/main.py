from fastapi import FastAPI

import uvicorn

from api import auth_router, hotel_router, room_router, booking_router


app = FastAPI()



        
app.include_router(auth_router)
app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(booking_router)


def main():
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    main()
