from fastapi import APIRouter

from .auth import router as auth_router
from .hotels import router as hotel_router
from .rooms import router as room_router
from .bookings import router as booking_router
from .facilities import router as facility_router


main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(hotel_router)
main_router.include_router(room_router)
main_router.include_router(booking_router)
main_router.include_router(facility_router)