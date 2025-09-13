from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from cur_user import get_current_user_id
from schemas.recipe_schema import RecipeCreate, RecipeUpdate, RecipeRead
from services.recipe_service import RecipeService
from database.database import get_db

recipe_router = APIRouter()

@recipe_router.post("/", response_model=RecipeRead)
async def create_recipe(
    data: RecipeCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = RecipeService(db)
    return await service.create_recipe(data, user_id)

@recipe_router.get("/{recipe_id}", response_model=RecipeRead)
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    service = RecipeService(db)
    return await service.get_recipe(recipe_id, with_relations=True)

@recipe_router.put("/{recipe_id}", response_model=RecipeRead)
async def update_recipe(recipe_id: int, data: RecipeUpdate,
                        user_id: int = Depends(get_current_user_id),
                        db: AsyncSession = Depends(get_db)):
    service = RecipeService(db)
    return await service.update_recipe(recipe_id, data, user_id)

@recipe_router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: int,
                        user_id: int = Depends(get_current_user_id),
                        db: AsyncSession = Depends(get_db)):
    service = RecipeService(db)
    await service.delete_recipe(recipe_id, user_id)
    return {"status": "deleted"}

@recipe_router.get("/", response_model=List[RecipeRead])
async def get_recipes(
    ids: Optional[List[int]] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    service = RecipeService(db)
    if ids:
        return await service.get_recipes_by_ids(ids)
    return []
