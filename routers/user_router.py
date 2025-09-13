from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from database.database import get_db
from schemas import UserCreate, UserRead
from schemas.user_schema import UserWithContent
from services.user_service import UserService
from cur_user import get_current_user

user_router = APIRouter()

@user_router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user = await service.register(user_in)
    return user


@user_router.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    token = await service.login(email=form_data.username, password=form_data.password)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=30*60,   
        secure=False,    
        samesite="lax"
    )
    return {"message": "Успешный вход"}


@user_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Вы вышли"}


@user_router.get("/me", response_model=UserWithContent)
async def read_current_user(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    return await service.get_user_with_content(current_user.id)


@user_router.get("/{user_id}", response_model=UserWithContent)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    return await service.get_user_with_content(user_id)


