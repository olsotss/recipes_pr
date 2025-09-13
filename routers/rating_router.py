from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from cur_user import get_current_user_id
from database.database import get_db
from schemas.rating_schema import RatingCreate, RatingRead
from services.rating_service import RatingService

rating_router = APIRouter()


@rating_router.post("/{recipe_id}", response_model=RatingRead)
async def rate_recipe(
    recipe_id: int = Path(..., description="ID рецепта"),
    data: RatingCreate = Depends(),  
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = RatingService(db)
    return await service.rate_recipe(recipe_id, user_id=user_id, value=data.value)


@rating_router.get("/{recipe_id}/average")
async def get_average_rating(
    recipe_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = RatingService(db)
    avg = await service.get_average_rating(recipe_id)
    return {"recipe_id": recipe_id, "average_rating": avg}


@rating_router.delete("/{recipe_id}")
async def delete_rating(
    recipe_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = RatingService(db)
    success = await service.delete_rating(recipe_id, user_id=user_id)
    if success:
        return {"detail": "Rating deleted"}
    return {"detail": "Rating not found"}
