from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, func
from database.database import Base
from sqlalchemy.orm import relationship
from models import collection_recipes

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    is_public = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="collections")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    recipes = relationship("Recipe", secondary=collection_recipes, back_populates="collections")
