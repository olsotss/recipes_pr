from typing import Dict, Any
from schemas.recipe_schema import RecipeCard
from schemas.feed_schema import FeedRequest
from repositories.feed_repository import FeedRepository
from sqlalchemy.ext.asyncio import AsyncSession

class FeedService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.feed_repo = FeedRepository(db)

    async def get_feed(self, params: FeedRequest) -> Dict[str, Any]:
        total, items = await self.feed_repo.get_feed(params)

        items_serialized = [
            RecipeCard(
                id=r.id,
                title=r.title,
                description=r.description,
                preview_image=r.image,
                average_rating=r.average_rating
            )
            for r in items
        ]

        return {
            "total": total,
            "items": items_serialized
        }
