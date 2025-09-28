from pydantic import BaseModel

class RatingCreate(BaseModel):
    recipe_id: int
    value: int 

class RatingRead(BaseModel):
    id: int
    recipe_id: int
    user_id: int
    value: int

    class Config:
        orm_mode = True


