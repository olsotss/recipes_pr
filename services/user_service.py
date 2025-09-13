from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repository import UserRepository
from schemas.user_schema import UserCreate, UserUpdate
from auth import create_access_token
from models import User

class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register(self, data: UserCreate) -> User:
        existing_user = await self.repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
        return await self.repo.create(data)

    async def login(self, email: str, password: str) -> str:
        user = await self.repo.authenticate(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверные данные для входа",
                headers={"WWW-Authenticate": "Bearer"}
            )
        token = create_access_token({"sub": str(user.id)})
        return token

    async def get_user(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user

    async def get_user_with_content(self, user_id: int) -> User:
        user = await self.repo.get_user_with_content(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user

    async def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = await self.repo.update(user_id, data)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user

    async def delete_user(self, user_id: int) -> None:
        deleted = await self.repo.delete(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
