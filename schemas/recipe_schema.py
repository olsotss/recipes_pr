from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class RecipeBase(BaseModel):
    title: str
    description: str
    ingredients: List[str] = []
    steps: str
    photo_url: str
    cooking_time: int

class RecipeCreate(RecipeBase):
    collection_ids: Optional[List[int]] = []

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[List[str]] = None
    steps: Optional[str] = None
    photo_url: Optional[str] = None
    cooking_time: Optional[int] = None
    collection_ids: Optional[List[int]] = None

class RecipeRead(RecipeBase):
    id: int
    user_id: int
    average_rating: Optional[float] = 0.0
    collections: List[str] = []
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
