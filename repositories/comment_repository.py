from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.comment_model import Comment
from models.recipe_model import Recipe
from schemas.comment_schema import CommentCreate, CommentUpdate

class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, recipe_id: int, user_id: int, data: CommentCreate) -> Optional[Comment]:
        exists = await self.db.execute(select(Recipe.id).filter(Recipe.id == recipe_id))

        if not exists.scalar_one_or_none:
            return None
        
        comment = Comment(**data.dict(), recipe_id = recipe_id, user_id = user_id)

        await self.db.commit()
        await self.db.refresh(comment)
        return comment
    
    async def get_comment_by_id(self, comment_id: int, with_author: bool = False) -> Optional[Comment]:
        stmt = select(Comment).filter(Comment.id == comment_id)

        if with_author:
            stmt = stmt.options(selectinload(Comment.user))
        
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_comment_by_recipe(self, recipe_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
        res = await self.db.execute(select(Comment)
                                    .filter(Comment.recipe_id == recipe_id)
                                    .order_by(Comment.created_at.desc())
                                    .offset(skip)
                                    .limit(limit))
        return res.scalars().all()
    
    async def update(self, comment_id: int, user_id: int, data: CommentUpdate) -> Optional[Comment]:
        comment = await self.get_comment_by_id(comment_id)
        if not comment or comment.user_id != user_id:
            return None

        for field, value in data.dict(exclude_unset=True).items():
            setattr(comment, field, value)

        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def delete(self, comment_id: int, user_id: int) -> bool:
        comment = await self.get_comment_by_id(comment_id)
        if not comment or comment.user_id != user_id:
            return False
        await self.db.delete(comment)
        await self.db.commit()
        return True

