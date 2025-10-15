from fastapi import APIRouter

from src.api.dependencies import DB_Dep
from schemas import FacilityRequestSchema, FacilityResponceSchema


router = APIRouter(prefix="/facilities", tags=["Удобства"])



@router.get("/")
async def get_all(
    db: DB_Dep
):
    facilities: list[FacilityResponceSchema] = await db.facility.get_all()
    
    return facilities


@router.post("/")
async def create(
    db: DB_Dep,
    facility_data: FacilityRequestSchema
):
    facility: FacilityResponceSchema = await db.facility.add(facility_data)
    await db.commit()
    
    return {"status": "ok", "data": facility}