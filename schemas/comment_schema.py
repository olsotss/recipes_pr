from datetime import datetime
from pydantic import BaseModel

from schemas.user_schema import UserRead

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    recipe_id: int

class CommentRead(CommentBase):
    id: int
    recipe_id: int
    user_id: int
    user: UserRead
    created_at: datetime
    
    class Config:
        orm_mode = True
