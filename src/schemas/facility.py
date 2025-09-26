from pydantic import Field

from core.schemas.base_schema import BaseModelSchema, BaseModel


class FacilityRequestSchema(BaseModel):
    title: str = Field(max_length=100)
    

class FacilityResponceSchema(BaseModelSchema):
    id: int
    title: str
    
    
class RoomFacilityAddSchema(BaseModel):
    room_id: int
    facility_id: int
    
class RoomFacilityResponceSchema(RoomFacilityAddSchema):
    id: int
    


