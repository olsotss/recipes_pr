from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Collection
from schemas import CollectionCreate, CollectionUpdate


class CollectionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, collection: Collection) -> Collection:
        self.db.add(collection)
        await self.db.commit()
        await self.db.refresh(collection)
        return collection

    async def get_collections_by_ids(self, ids: List[int]) -> List[Collection]:
        if not ids:
            return []
        stmt = select(Collection).filter(Collection.id.in_(ids))
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def get_by_id(self, collection_id: int, with_recipes: bool = False) -> Optional[Collection]:
        stmt = select(Collection).filter(Collection.id == collection_id)
        if with_recipes:
            stmt = stmt.options(selectinload(Collection.recipes))
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def list_user_collections(self, user_id: int) -> List[Collection]:
        res = await self.db.execute(select(Collection).filter(Collection.user_id == user_id))
        return res.scalars().all()

    async def update(self, collection: Collection) -> Collection:
        self.db.add(collection)
        await self.db.commit()
        await self.db.refresh(collection)
        return collection

    async def delete(self, collection: Collection) -> None:
        await self.db.delete(collection)
        await self.db.commit()


