from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from models.collection_model import Collection
from repositories.collection_repository import CollectionRepository
from schemas.collection_schema import CollectionCreate, CollectionUpdate


class CollectionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.collection_repo = CollectionRepository(db)

    async def get_collection(self, collection_id: int, with_recipes: bool = False) -> Collection:
        collection = await self.collection_repo.get_by_id(collection_id, with_recipes=with_recipes)

        if not collection:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
        
        return collection

    async def get_collections_by_ids(self, ids: List[int], with_recipes: bool = False) -> List[Collection]:
        return await self.collection_repo.get_collections_by_ids(ids, with_recipes=with_recipes)

    async def create_collection(self, data: CollectionCreate, user_id: int) -> Collection:
        return await self.collection_repo.create(user_id, data)

    async def update_collection(self, collection_id: int, user_id: int, data: CollectionUpdate) -> Collection:
        collection = await self.collection_repo.get_by_id(collection_id, with_recipes=True)

        if not collection:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
        
        if collection.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot edit this collection")

        updated_collection = await self.collection_repo.update(collection_id, user_id, data)

        if not updated_collection:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update collection")
        
        return updated_collection

    async def delete_collection(self, collection_id: int, user_id: int) -> None:
        collection = await self.collection_repo.get_by_id(collection_id)

        if not collection:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
        
        if collection.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot delete this collection")

        success = await self.collection_repo.delete(collection_id, user_id)

        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete collection")

    async def add_recipe_to_collection(self, collection_id: int, user_id: int, recipe_id: int) -> Collection:
        collection = await self.collection_repo.add_recipe(collection_id, user_id, recipe_id)

        if not collection:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection or recipe not found")
        
        return collection

    async def remove_recipe_from_collection(self, collection_id: int, user_id: int, recipe_id: int) -> Collection:
        collection = await self.collection_repo.remove_recipe(collection_id, user_id, recipe_id)

        if not collection:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection or recipe not found")
        
        return collection
