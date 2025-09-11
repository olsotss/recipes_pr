from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

from schemas.collection_schema import CollectionRead

class RecipeBase(BaseModel):
    title: str
    description: str
    ingredients: List[str] = []
    steps: str
    image: str
    cooking_time: int

class RecipeCreate(RecipeBase):
    collection_ids: Optional[List[int]] = []

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[List[str]] = None
    steps: Optional[str] = None
    image: Optional[str] = None
    cooking_time: Optional[int] = None
    collection_ids: Optional[List[int]] = None

class RecipeRead(RecipeBase):
    id: int
    user_id: int
    average_rating: Optional[float] = 0.0
    collections: List[CollectionRead] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RecipeCard(BaseModel):
    id: int
    title: str
    description: str
    preview_image: Optional[str] = None
    average_rating: Optional[float] = None
    
    class Config:
        orm_mode = True
