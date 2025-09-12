from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from repositories.comment_repository import CommentRepository
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
async def get_comments(
    recipe_id: int,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = Query("created_at", description="Поле для сортировки: created_at или rating"),
    sort_order: str = Query("desc", description="Порядок сортировки: asc или desc"),
    db: AsyncSession = Depends(get_db)
):
    comment_repo = CommentRepository(db)
    comments = await comment_repo.get_comment_by_recipe(
        recipe_id=recipe_id,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return comments


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
    try:
        await service.delete_comment(comment_id, user_id=1)
        return {"detail": "Comment deleted"}
    except HTTPException as e:
        raise e
