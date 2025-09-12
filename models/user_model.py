from sqlalchemy import Column, DateTime, Integer, String, func
from database.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    recipes = relationship("Recipe", back_populates="user", cascade="all, delete", lazy="selectin")
    comments = relationship("Comment", back_populates="user", cascade="all, delete", lazy="selectin")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete", lazy="selectin")
    collections = relationship("Collection", back_populates="user", cascade="all, delete", lazy="selectin")

