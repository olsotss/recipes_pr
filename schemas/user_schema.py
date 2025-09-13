from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from schemas.collection_schema import CollectionRead
from schemas.recipe_schema import RecipeCard

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str 


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserShort(BaseModel):
    id: int
    email: EmailStr
    username: str

    class Config:
        orm_mode = True

class UserWithContent(BaseModel):
    id: int
    username: str
    collections: List[CollectionRead] = []
    recipes: List[RecipeCard] = []

    class Config:
        from_attributes = True
