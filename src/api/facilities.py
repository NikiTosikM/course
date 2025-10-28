from fastapi import APIRouter

from src.api.dependencies import DB_Dep
from src.schemas import FacilityRequestSchema, FacilityResponceSchema
from src.service.facility_service import FacilityService


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/")
async def get_all(db: DB_Dep):
    facilities: list[FacilityResponceSchema] = await FacilityService(db).get_all_facilities()

    return facilities


@router.post("/")
async def create(db: DB_Dep, facility_data: FacilityRequestSchema):
    facility = await FacilityService(db).create_facility(facility_data)

    return {"status": "ok", "data": facility}
