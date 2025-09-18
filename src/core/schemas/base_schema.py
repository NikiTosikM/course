from pydantic import BaseModel


class BaseModelSchema(BaseModel):
    class Config:
        from_attributes = True