from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import User
from schemas.user_schema import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, data: UserCreate) -> User:
        user = User(**data.dict())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 10) -> List[User]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def update(self, user_id: int, data: UserUpdate) -> Optional[User]:
        user = await self.get_user_by_id(user_id)

        if not user:
            return None
        
        for field, value in data.dict(exclude_unset=True).items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_user_by_id(user_id)

        if user:
            await self.db.delete(user)
            await self.db.commit()
            return True
        
        return False