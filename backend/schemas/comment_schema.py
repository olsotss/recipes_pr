from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from schemas.user_schema import UserShort

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    text: Optional[str] = None

    class Config:
        orm_mode = True

class CommentRead(CommentBase):
    id: int
    recipe_id: int
    user: UserShort
    created_at: datetime
    
    class Config:
        orm_mode = True
