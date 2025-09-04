from sqlalchemy.ext.asyncio import AsyncSession
from repositories.rating_repository import RatingRepository
from models.rating_model import Rating

class RatingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.rating_repo = RatingRepository(db)

    async def rate_recipe(self, recipe_id: int, user_id: int, value: int) -> Rating:
        return await self.rating_repo.rate_recipe(recipe_id, user_id, value)

    async def get_average_rating(self, recipe_id: int) -> float:
        return await self.rating_repo.get_average_rating(recipe_id)

    async def delete_rating(self, recipe_id: int, user_id: int) -> bool:
        return await self.rating_repo.delete(recipe_id, user_id)

    async def recalc_average_rating(self, recipe_id: int) -> float:
        return await self.rating_repo.recalc_avg_rating(recipe_id)
