from typing import List, Tuple
from sqlalchemy import and_, asc, desc, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.recipe_model import Recipe
from schemas.feed_schema import FeedRequest

class FeedRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_feed(self, params: FeedRequest) -> Tuple[int, List[Recipe]]:
        base_query = select(Recipe)
        count_query = select(func.count(Recipe.id))

        filters = []

        if params.title:
            filters.append(Recipe.title.ilike(f"%{params.title}%"))

        if params.ingredients:
            or_clauses = [Recipe.ingredients.contains([i]) for i in params.ingredients]
            filters.append(or_(*or_clauses))

        if params.author_id:
            filters.append(Recipe.user_id == params.author_id)

        if params.min_rating:
            filters.append(Recipe.average_rating >= params.min_rating)

        if filters:
            base_query = base_query.filter(and_(*filters))
            count_query = count_query.filter(and_(*filters))

        order_field = {
            "date": Recipe.created_at,
            "rating": Recipe.average_rating,
            "title": Recipe.title
        }[params.sort_by]

        direction = desc if params.order == "desc" else asc
        base_query = base_query.order_by(direction(order_field))

        total = (await self.db.execute(count_query)).scalar_one()

        base_query = base_query.offset(params.skip).limit(params.limit)
        result = await self.db.execute(base_query)
        items = result.scalars().all()

        return total, items