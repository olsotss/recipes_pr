from pydantic import BaseModel

class RatingCreate(BaseModel):
    recipe_id: int
    score: int 

class RatingRead(BaseModel):
    id: int
    recipe_id: int
    user_id: int
    score: int

    class Config:
        orm_mode = True


