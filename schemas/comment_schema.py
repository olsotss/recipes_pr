from pydantic import BaseModel

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    recipe_id: int

class CommentRead(CommentBase):
    id: int
    recipe_id: int
    user_id: int

    class Config:
        orm_mode = True
