from pydantic import BaseModel
from typing import List, Optional

class CollectionBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_public: bool = True

class CollectionCreate(CollectionBase):
    recipe_ids: List[int] = []

class CollectionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    recipe_ids: Optional[List[int]] = None

class CollectionRead(CollectionBase):
    id: int
    user_id: int
    recipes: List[str] = [] 

    class Config:
        orm_mode = True
