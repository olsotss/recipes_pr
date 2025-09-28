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

        if not exists.scalar_one_or_none():
            return None
    
        comment = Comment(**data.dict(), recipe_id=recipe_id, user_id=user_id)
    
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)
        
        stmt = select(Comment).options(selectinload(Comment.user)).filter(Comment.id == comment.id)
        res = await self.db.execute(stmt)
        comment_with_user = res.scalar_one()
    
        return comment_with_user
    
    async def get_comment_by_id(self, comment_id: int, with_author: bool = False) -> Optional[Comment]:
        stmt = select(Comment).filter(Comment.id == comment_id)

        if with_author:
            stmt = stmt.options(selectinload(Comment.user))
        
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_comment_by_recipe(self, recipe_id: int, skip: int = 0, limit: int = 10, sort_by: str = "created_at", sort_order: str = "desc") -> List[Comment]:
        if sort_by == "created_at":
            order_column = Comment.created_at

        if sort_order == "desc":
            order_column = order_column.desc()
        else:
            order_column = order_column.asc()

        stmt = (
            select(Comment)
            .filter(Comment.recipe_id == recipe_id)
            .order_by(order_column)
            .offset(skip)
            .limit(limit)
        )

        res = await self.db.execute(stmt)
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

