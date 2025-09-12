from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from models.collection_model import Collection
from models.recipe_model import Recipe
from repositories.collection_repository import CollectionRepository
from repositories.recipe_repository import RecipeRepository
from schemas.collection_schema import CollectionCreate, CollectionUpdate


class CollectionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.collection_repo = CollectionRepository(db)
        self.recipe_repo = RecipeRepository(db)

    async def get_collection(self, collection_id: int, with_recipes: bool = False) -> Collection:
        collection = await self.collection_repo.get_by_id(collection_id, with_recipes=with_recipes)

        if not collection:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")

        return collection

    async def get_collections_by_ids(self, ids: List[int], with_recipes: bool = False) -> List[Collection]:
        return await self.collection_repo.get_collections_by_ids(ids)

    async def create_collection(self, data: CollectionCreate, user_id: int) -> Collection:
        collection = Collection(**data.dict(exclude={"recipe_ids"}), user_id=user_id)

        if data.recipe_ids:
            recipes = await self.recipe_repo.get_recipes_by_ids(data.recipe_ids)
            collection.recipes = recipes

        return await self.collection_repo.create(collection)

    async def update_collection(self, collection_id: int, user_id: int, data: CollectionUpdate) -> Collection:
        collection = await self.collection_repo.get_by_id(collection_id, with_recipes=True)

        if not collection:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")

        if collection.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot edit this collection")

        payload = data.dict(exclude_unset=True, exclude={"recipe_ids"})
        for field, value in payload.items():
            setattr(collection, field, value)

        if data.recipe_ids is not None:
            recipes = await self.recipe_repo.get_recipes_by_ids(data.recipe_ids)
            collection.recipes = recipes

        return await self.collection_repo.update(collection)

    async def delete_collection(self, collection_id: int, user_id: int) -> None:
        collection = await self.collection_repo.get_by_id(collection_id)

        if not collection:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")

        if collection.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot delete this collection")

        await self.collection_repo.delete(collection)

    async def add_recipe_to_collection(self, collection_id: int, user_id: int, recipe_id: int) -> Collection:
        collection = await self.collection_repo.get_by_id(collection_id, with_recipes=True)

        if not collection or collection.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")

        recipe = await self.recipe_repo.get_recipe(recipe_id)
        if not recipe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

        if recipe not in collection.recipes:
            collection.recipes.append(recipe)

        return await self.collection_repo.update(collection)

    async def remove_recipe_from_collection(self, collection_id: int, user_id: int, recipe_id: int) -> Collection:
        collection = await self.collection_repo.get_by_id(collection_id, with_recipes=True)

        if not collection or collection.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")

        collection.recipes = [r for r in collection.recipes if r.id != recipe_id]

        return await self.collection_repo.update(collection)
