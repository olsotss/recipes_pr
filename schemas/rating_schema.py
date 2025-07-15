from pydantic import BaseModel

class RatingCreate(BaseModel):
    recipe_id: int
    value: int 
