from os import access
from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr
from sqlalchemy import orm

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    class Config:
        orm_mode = True

class PostUser(BaseModel):
    id : int
    email: str
    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    owner_id : int
    owner : PostUser
    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email : EmailStr
    password : str



class UserLogin(CreateUser):
    pass

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None


######################### vote router

class LikeInput(BaseModel):
    post_id : int
    vote_dir : int 
    