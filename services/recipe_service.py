from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.recipe_model import Recipe
from repositories.recipe_repository import RecipeRepository
from repositories.collection_repository import CollectionRepository
from schemas.recipe_schema import RecipeCreate, RecipeUpdate

class RecipeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.recipe_repo = RecipeRepository(db)
        self.collection_repo = CollectionRepository(db)

    async def get_recipe(self, recipe_id: int, with_relations: bool = False) -> Recipe:
        recipe = await self.recipe_repo.get_recipe_by_id(recipe_id, with_relations=with_relations)
        if not recipe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
        return recipe

    async def get_recipes_by_ids(self, ids: List[int]) -> List[Recipe]:
        return await self.recipe_repo.get_recipes_by_ids(ids)

    async def create_recipe(self, data: RecipeCreate, user_id: int) -> Recipe:
        # создаем объект с user_id
        recipe = Recipe(**data.dict(exclude={"collection_ids"}), user_id=user_id)

        # Сначала добавляем рецепт в сессию, чтобы он имел PK
        self.db.add(recipe)
        await self.db.flush()

        # Присваиваем коллекции (если есть)
        if data.collection_ids:
            collections = await self.collection_repo.get_collections_by_ids(data.collection_ids)
            recipe.collections = collections

        await self.db.commit()
        await self.db.refresh(recipe)
        return recipe

    async def update_recipe(self, recipe_id: int, data: RecipeUpdate, user_id: int) -> Recipe:
        recipe = await self.recipe_repo.get_recipe_by_id(recipe_id, with_relations=True)
        if not recipe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
        if recipe.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot edit this recipe")

        payload = data.dict(exclude_unset=True, exclude={"collection_ids"})
        for field, value in payload.items():
            setattr(recipe, field, value)

        if data.collection_ids is not None:
            collections = await self.collection_repo.get_collections_by_ids(data.collection_ids)
            recipe.collections = collections

        await self.db.commit()
        await self.db.refresh(recipe)
        return recipe

    async def delete_recipe(self, recipe_id: int, user_id: int):
        recipe = await self.recipe_repo.get_recipe_by_id(recipe_id)
        if not recipe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
        if recipe.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot delete this recipe")
        await self.recipe_repo.delete(recipe)
