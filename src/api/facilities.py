from fastapi import APIRouter


from api.dependencies import DB_Dep
from schemas import FacilityRequestSchema, FacilityResponceSchema


router = APIRouter(prefix="/facilities", tags=["Удобства"])



@router.get("/")
# @cache(expire=5)
async def get_all(
    db: DB_Dep
):
    return await db.facility.get_all()


@router.post("/")
async def create(
    db: DB_Dep,
    facility_data: FacilityRequestSchema
):
    facility: FacilityResponceSchema = await db.facility.add(facility_data)
    await db.commit()
    
    return {"status": "ok", "data": facility}