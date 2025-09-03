from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.collection_model import Collection
from repositories.recipe_repository import RecipeRepository
from schemas.collection_schema import CollectionCreate, CollectionUpdate

class CollectionRepository:
    def __init__(self, db: AsyncSession, recipe_repo: RecipeRepository):
        self.db = db
        self.recipe_repo = recipe_repo

    async def create(self, user_id: int, data: CollectionCreate) -> Collection:
        collection = Collection(**data.dict(exclude={"recipe_ids"}), user_id=user_id)

        if data.recipe_ids:
            recipes = await self.recipe_repo.get_recipes_by_ids(data.recipe_ids)
            collection.recipes = recipes
        
        self.db.add(collection)
        await self.db.commit()
        await self.db.refresh(collection)
        return collection
    
    async def get_by_id(self, collection_id: int, with_recipes: bool = False) -> Optional[Collection]:
        stmt = select(Collection).filter(Collection.id == collection_id)
        if with_recipes:
            stmt = stmt.options(selectinload(Collection.recipes))
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
            
    async def list_user_collections(self, user_id: int) -> List[Collection]:
        res = await self.db.execute(select(Collection).filter(Collection.user_id == user_id))
        return res.scalars().all()
    
    async def update(self, collection_id: int, user_id: int, data: CollectionUpdate) -> Optional[Collection]:
        collection = await self.get_by_id(collection_id, with_recipes=True)

        if not collection or collection.user_id != user_id:
            return None

        payload = data.dict(exclude_unset=True, exclude={"recipe_ids"})

        for field, value in payload.items():
            setattr(collection, field, value)

        if data.recipe_ids is not None:
            recipes = await self.recipe_repo.get_recipes_by_ids(data.recipe_ids)
            collection.recipes = recipes

        await self.db.commit()
        await self.db.refresh(collection)

        return collection

    async def delete(self, collection_id: int, user_id: int) -> bool:
        collection = await self.get_by_id(collection_id)

        if not collection or collection.user_id != user_id:
            return False
        
        await self.db.delete(collection)
        await self.db.commit()

        return True

    async def add_recipe(self, collection_id: int, user_id: int, recipe_id: int) -> Optional[Collection]:
        collection = await self.get_by_id(collection_id, with_recipes=True)
        if not collection or collection.user_id != user_id:
            return None

        recipe = await self.recipe_repo.get_recipe(recipe_id)

        if not recipe:
            return None

        if recipe not in collection.recipes:
            collection.recipes.append(recipe)

        await self.db.commit()
        await self.db.refresh(collection)

        return collection

    async def remove_recipe(self, collection_id: int, user_id: int, recipe_id: int) -> Optional[Collection]:
        collection = await self.get_by_id(collection_id, with_recipes=True)

        if not collection or collection.user_id != user_id:
            return None

        collection.recipes = [i for i in collection.recipes if i.id != recipe_id]

        await self.db.commit()
        await self.db.refresh(collection)
        return collection
