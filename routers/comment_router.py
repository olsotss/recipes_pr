from fastapi import APIRouter, Body, Depends, Path, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from schemas.comment_schema import CommentCreate, CommentUpdate, CommentRead
from services.comment_service import CommentService

comment_router = APIRouter()


@comment_router.post("/recipes/{recipe_id}", response_model=CommentRead)
async def add_comment(
    recipe_id: int = Path(..., description="ID рецепта"),
    data: CommentCreate = Body(...),
    db: AsyncSession = Depends(get_db),
):
    service = CommentService(db)
    comment = await service.add_comment(recipe_id, user_id=1, data=data)
    return comment


@comment_router.get("/{comment_id}", response_model=CommentRead)
async def get_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = CommentService(db)
    return await service.get_comment(comment_id, with_author=True)


@comment_router.get("/recipes/{recipe_id}", response_model=List[CommentRead])
async def get_comments_for_recipe(
    recipe_id: int,
    skip: int = Query(0, description="Сколько пропустить"),
    limit: int = Query(10, description="Сколько вернуть"),
    db: AsyncSession = Depends(get_db),
):
    service = CommentService(db)
    return await service.get_comments_by_recipe(recipe_id, skip=skip, limit=limit)


@comment_router.put("/{comment_id}", response_model=CommentRead)
async def update_comment(
    comment_id: int,
    data: CommentUpdate = Depends(),
    db: AsyncSession = Depends(get_db),
):
    service = CommentService(db)
    return await service.update_comment(comment_id, user_id=1, data=data)


@comment_router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = CommentService(db)
    success = await service.delete_comment(comment_id, user_id=1)
    if success:
        return {"detail": "Comment deleted"}
    return {"detail": "Comment not found"}
