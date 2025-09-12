from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from models.recipe_model import Recipe

class RecipeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_recipe_by_id(self, recipe_id: int, with_relations: bool = False) -> Optional[Recipe]:
        stmt = select(Recipe).filter(Recipe.id == recipe_id)
        if with_relations:
            stmt = stmt.options(
                selectinload(Recipe.collections),
                selectinload(Recipe.comments)
            )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_recipes_by_ids(self, ids: List[int]) -> List[Recipe]:
        if not ids:
            return []
        stmt = select(Recipe).filter(Recipe.id.in_(ids))
        stmt = stmt.options(
            selectinload(Recipe.collections),
            selectinload(Recipe.comments)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, recipe: Recipe) -> Recipe:
        self.db.add(recipe)
        await self.db.commit()
        await self.db.refresh(recipe)
        return recipe

    async def update(self, recipe: Recipe) -> Recipe:
        self.db.add(recipe)
        await self.db.commit()
        await self.db.refresh(recipe)
        return recipe

    async def delete(self, recipe: Recipe) -> None:
        await self.db.delete(recipe)
        await self.db.commit()
