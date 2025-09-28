from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.rating_model import Rating
from models.recipe_model import Recipe
from repositories.recipe_repository import RecipeRepository

class RatingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.recipe_repo = RecipeRepository(db)

    async def recalc_avg_rating(self, recipe_id: int) -> float:
        avg_stmt = select(func.avg(Rating.value)).filter(Rating.recipe_id == recipe_id)
        avg = (await self.db.execute(avg_stmt)).scalar()
        avg = float(avg) if avg is not None else 0.0

        result = await self.db.execute(
            select(Recipe).filter(Recipe.id == recipe_id).with_for_update()
        )
        recipe = result.scalar_one_or_none()

        recipe = await self.recipe_repo.get_recipe_by_id(recipe_id)
        
        if  recipe:
            recipe.average_rating = avg
            await self.db.commit()
        
        return avg
    
    async def rate_recipe(self, recipe_id: int, user_id: int, value: int) -> Rating:
        res = await self.db.execute(
            select(Rating).filter(Recipe.id == recipe_id, Rating.user_id == user_id)
        )
        rating = res.scalar_one_or_none()

        if rating:
            rating.value = value
        else:
            rating = Rating(recipe_id=recipe_id, user_id=user_id, value=value)
            self.db.add(rating)
        
        await self.db.commit()
        await self.db.refresh(rating)

        await self.recalc_avg_rating(recipe_id)

        return rating

    async def get_average_rating(self, recipe_id: int) -> float:
        res = await self.db.execute(
            select(func.avg(Rating.value)).filter(Rating.recipe_id == recipe_id)
        )
        avg = res.scalar()
        return float(avg) if avg is not None else 0.0

    async def delete(self, recipe_id: int, user_id: int) -> bool:
        res = await self.db.execute(
            select(Rating).filter(Rating.recipe_id == recipe_id, Rating.user_id == user_id)
        )
        rating = res.scalar_one_or_none()

        if not rating:
            return False
        
        await self.db.delete(rating)
        await self.db.commit()

        await self.recalc_avg_rating(recipe_id)
        
        return True