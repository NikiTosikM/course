from repositories.base_repository import BaseRepository

from models.facilities import Facilities
from schemas.facility import FacilityResponceSchema


class FacilityRepository(BaseRepository[Facilities]):
    model = Facilities
    schema = FacilityResponceSchema
    
    
    