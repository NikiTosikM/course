from pydantic import Field

from src.core.schemas.base_schema import BaseModelSchema, BaseModel


class FacilityRequestSchema(BaseModelSchema):
    title: str = Field(max_length=100)
    

class FacilityResponceSchema(FacilityRequestSchema):
    id: int
    
    
class RoomFacilityAddSchema(BaseModel):
    room_id: int
    facility_id: int
    
class RoomFacilityResponceSchema(RoomFacilityAddSchema):
    id: int
    


