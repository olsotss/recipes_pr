from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.recipe_model import Recipe
from collection_repository import CollectionRepository
from schemas.recipe_schema import RecipeCreate, RecipeUpdate

class RecipeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_recipes_by_ids(self, ids: List[int]) -> List[Recipe]:
        if not ids:
            return []
        res = await self.db.execute(select(Recipe).filter(Recipe.id.in_(ids)))
        return res.scalars().all()

    async def get_recipe(self, recipe_id: int) -> Optional[Recipe]:
        res = await self.db.execute(select(Recipe).filter(Recipe.id == recipe_id))
        return res.scalar_one_or_none()
    
    async def get_recipe_by_id(self, recipe_id: int, with_relations: bool = False) -> Recipe | None:
        res1 = select(Recipe).filter(Recipe.id == recipe_id)

        if with_relations:
            res1 = res1.options(
                selectinload(Recipe.collections),
            )
            
        res = await self.db.execute(res1)
        return res.scalar_one_or_none()


    async def create(self, data: RecipeCreate, user_id: int) -> Recipe:
        recipe = Recipe(**data.dict(exclude={"collection_ids"}), user_id=user_id)

        if data.collection_ids:
            collection_repo = CollectionRepository(self.db)
            collections = await collection_repo.get_collections_by_ids(data.collection_ids)
            recipe.collections = collections

        self.db.add(recipe)
        await self.db.commit()
        await self.db.refresh(recipe)
        return recipe
    
    async def update(self, recipe_id: int, data: RecipeUpdate) -> Optional[Recipe]:
        recipe = await self.get_recipe_by_id(recipe_id, with_relations=True)

        if not recipe:
            return None
        
        if data.collection_ids:
            collection_repo = CollectionRepository(self.db)
            collections = await collection_repo.get_collections_by_ids(data.collection_ids)
            recipe.collections = collections
        
        payload = data.dict(exclude_unset=True, exclude={"collection_ids"})

        for field, value in payload.items():
            setattr(recipe, field, value)
        
        await self.db.commit()
        await self.db.refresh(recipe)
        return recipe

    async def delete(self, recipe_id: int) -> bool:
        recipe = await self.get_recipe_by_id(recipe_id)

        if not recipe:
            return False
        
        await self.db.delete(recipe)
        await self.db.commit()
        return True
