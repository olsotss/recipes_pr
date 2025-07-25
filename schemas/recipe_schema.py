from pydantic import BaseModel
from typing import Optional, List

class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    ingredients: List[str]
    steps: str
    image: Optional[str] = None

class RecipeCreate(RecipeBase):
    tag_ids: List[int] = []

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[List[str]] = None
    steps: Optional[str] = None
    image: Optional[str] = None
    tag_ids: Optional[List[int]] = None

class RecipeRead(RecipeBase):
    id: int
    average_rating: float
    author_id: int
    tags: List[str] = []

    class Config:
        orm_mode = True


