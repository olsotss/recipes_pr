from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Float, func
from database.database import Base
from sqlalchemy.orm import relationship
from models import recipe_tags, collection_recipes

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    ingredients = Column(Text)
    steps = Column(Text)
    image = Column(String)
    average_rating = Column(Float, default=0.0)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="recipes")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    comments = relationship("Comment", back_populates="recipe", cascade="all, delete")
    ratings = relationship("Rating", back_populates="recipe", cascade="all, delete")
    collections = relationship("Collection", secondary=collection_recipes, back_populates="recipes")
