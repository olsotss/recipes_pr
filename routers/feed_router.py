from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.feed_schema import FeedRequest, FeedResponse
from database.database import get_db
from services.feed_service import FeedService

feed_router = APIRouter()

@feed_router.get("/", response_model=FeedResponse)
async def get_feed(
    title: str = Query(None, description="Поиск по названию рецепта"),
    ingredients: List[str] = Query(None, description="Фильтр по ингредиентам"),
    author_id: int = Query(None, description="Фильтр по автору"),
    min_rating: float = Query(None, description="Минимальный рейтинг"),
    sort_by: str = Query("date", description="Сортировка: date, rating, title"),
    order: str = Query("desc", description="Порядок сортировки: asc или desc"),
    skip: int = Query(0, description="Количество пропущенных записей"),
    limit: int = Query(10, description="Количество записей для выдачи"),
    db: AsyncSession = Depends(get_db),
):
    params = FeedRequest(
        title=title,
        ingredients=ingredients,
        author_id=author_id,
        min_rating=min_rating,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=limit
    )

    service = FeedService(db)
    total, items = await service.get_feed(params)
    return FeedResponse(total=total, items=items)
