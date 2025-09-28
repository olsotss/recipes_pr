from fastapi import HTTPException, status, Depends, Cookie, Request
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repository import UserRepository
from models import User
from database.database import get_db
from auth import decode_access_token
from jose import jwt, JWTError
from typing import Optional


async def get_current_user(access_token: str | None = Cookie(default=None), db: AsyncSession = Depends(get_db)) -> User:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Нет токена")

    try:
        payload = decode_access_token(access_token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен")

    repo = UserRepository(db)
    user = await repo.get_by_id(int(user_id))

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
        
    return user

def get_current_user_id(request: Request) -> int:
    from dotenv import load_dotenv
    import os

    load_dotenv()

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    
    token: Optional[str] = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Нет токена авторизации"
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный токен"
            )
        return int(user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен"
        )
