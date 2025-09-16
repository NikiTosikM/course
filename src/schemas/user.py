from pydantic import BaseModel, EmailStr, Field


class UserRequestSchema(BaseModel):
    name: str = Field(min_length=5)
    email: EmailStr
    password: str = Field(min_length=5)
    
    
class UserDBSchema(BaseModel):
    name: str = Field(min_length=5)
    email: EmailStr
    hashpassword: str
    

class UserResponceSchema(BaseModel):
    id: int
    email: EmailStr
    name: str
    
    class Config:
        from_attributes = True
        

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str