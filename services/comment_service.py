from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from models.comment_model import Comment
from repositories.comment_repository import CommentRepository
from schemas.comment_schema import CommentCreate, CommentUpdate


class CommentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.comment_repo = CommentRepository(db)

    async def add_comment(self, recipe_id: int, user_id: int, data: CommentCreate) -> Comment:
        comment = await self.comment_repo.add(recipe_id, user_id, data)

        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
        
        return comment

    async def get_comment(self, comment_id: int, with_author: bool = False) -> Comment:
        comment = await self.comment_repo.get_comment_by_id(comment_id, with_author=with_author)

        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        
        return comment

    async def get_comments_by_recipe(self, recipe_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
        return await self.comment_repo.get_comment_by_recipe(recipe_id, skip, limit)

    async def update_comment(self, comment_id: int, user_id: int, data: CommentUpdate) -> Comment:
        comment = await self.comment_repo.update(comment_id, user_id, data)

        if not comment:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot edit this comment")
        
        return comment

    async def delete_comment(self, comment_id: int, user_id: int) -> None:
        success = await self.comment_repo.delete(comment_id, user_id)
        
        if not success:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot delete this comment")
