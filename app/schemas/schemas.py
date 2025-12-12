from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

# Pydantic schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    
    id:int
    create_at:datetime

    class Config:
        orm_mode = True    



class UserBase(BaseModel):
    email:EmailStr
    password:str


class UserCreate(UserBase):
    pass            


class UserResponse(BaseModel):
    
    id:int
    email:EmailStr
    create_at: datetime   


    class Config:
        orm_mode = True    



class UserLogin(BaseModel):
    email:EmailStr
    password:str


class token(BaseModel):
    access_token: str
    token_type:str

class token_data(BaseModel):
    id: Optional[int]
