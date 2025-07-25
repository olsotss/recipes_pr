from typing import List, Optional, Literal
from pydantic import BaseModel

from schemas.recipe_schema import RecipeCard

class RecipeSearchFilters(BaseModel):
    title: Optional[str] = None
    ingredients: Optional[List[str]] = None
    author_id: Optional[int] = None
    collection_id: Optional[int] = None
    min_rating: Optional[float] = None

    sort_by: Literal["date", "rating", "title"] = "date"
    order: Literal["asc", "desc"] = "desc"

class Pagination(BaseModel):
    skip: int = 0
    limit: int = 10

class FeedRequest(RecipeSearchFilters, Pagination):
    pass

class FeedResponse(BaseModel):
    total: int         
    items: List[RecipeCard]  
    