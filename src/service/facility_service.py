from src.schemas.facility import FacilityRequestSchema, FacilityResponceSchema
from src.service.base_service import BaseService


class FacilityService(BaseService):
    async def get_all_facilities(self):
        facilities: list[FacilityResponceSchema] = await self.manager.facility.get_all()
        
        return facilities
    
    async def create_facility(self, facility_data: FacilityRequestSchema):
        facility: FacilityResponceSchema = await self.manager.facility.add(facility_data)
    
        await self.manager.commit()
        
        return facility