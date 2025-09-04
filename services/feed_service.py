from sqlalchemy.ext.asyncio import AsyncSession
from repositories.feed_repository import FeedRepository
from schemas.feed_schema import FeedRequest
from typing import Dict, Any


class FeedService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.feed_repo = FeedRepository(db)

    async def get_feed(self, params: FeedRequest) -> Dict[str, Any]:
        total, items = await self.feed_repo.get_feed(params)
        return {
            "total": total,
            "items": items
        }
