from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from schemas.collection_schema import CollectionCreate, CollectionUpdate, CollectionRead
from services.collection_service import CollectionService
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

def get_current_user_id() -> int:
    return 1

collection_router = APIRouter()

def get_collection_service(db: AsyncSession = Depends(get_db)) -> CollectionService:
    return CollectionService(db)


@collection_router.post("/", response_model=CollectionRead)
async def create_collection(
    data: CollectionCreate,
    user_id: int = Depends(get_current_user_id),
    service: CollectionService = Depends(get_collection_service),
):
    return await service.create_collection(user_id, data)


@collection_router.get("/", response_model=List[CollectionRead])
async def list_collections(
    service: CollectionService = Depends(get_collection_service),
):
    return await service.get_all()


@collection_router.get("/{collection_id}", response_model=CollectionRead)
async def get_collection(
    collection_id: int,
    service: CollectionService = Depends(get_collection_service),
):
    collection = await service.get_collections_by_ids(collection_id, with_recipes=True)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@collection_router.put("/{collection_id}", response_model=CollectionRead)
async def update_collection(
    collection_id: int,
    data: CollectionUpdate,
    user_id: int = Depends(get_current_user_id),
    service: CollectionService = Depends(get_collection_service),
):
    updated = await service.update(collection_id, user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Collection not found or not allowed")
    return updated


@collection_router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(
    collection_id: int,
    user_id: int = Depends(get_current_user_id),
    service: CollectionService = Depends(get_collection_service),
):
    deleted = await service.delete(collection_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Collection not found or not allowed")
    return None


@collection_router.post("/{collection_id}/recipes/{recipe_id}", response_model=CollectionRead)
async def add_recipe_to_collection(
    collection_id: int,
    recipe_id: int,
    user_id: int = Depends(get_current_user_id),
    service: CollectionService = Depends(get_collection_service),
):
    updated = await service.add_recipe(collection_id, user_id, recipe_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Collection not found or not allowed")
    return updated


@collection_router.delete("/{collection_id}/recipes/{recipe_id}", response_model=CollectionRead)
async def remove_recipe_from_collection(
    collection_id: int,
    recipe_id: int,
    user_id: int = Depends(get_current_user_id),
    service: CollectionService = Depends(get_collection_service),
):
    updated = await service.remove_recipe(collection_id, user_id, recipe_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Collection not found or not allowed")
    return updated
