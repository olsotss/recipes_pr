from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import User
from schemas.user_schema import UserCreate, UserUpdate
from auth import hash_password, verify_password

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: UserCreate) -> User:
        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hash_password(data.password)
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).filter(User.id == user_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).filter(User.email == email)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_user_with_content(self, user_id: int):
        stmt = select(User).options(
            selectinload(User.recipes),
            selectinload(User.collections)
        ).filter(User.id == user_id)

        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def update(self, user_id: int, data: UserUpdate) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if not user:
            return None
        for field, value in data.dict(exclude_unset=True).items():
            if field == "password":
                setattr(user, "hashed_password", hash_password(value))
            else:
                setattr(user, field, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
