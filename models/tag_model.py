from sqlalchemy import Column, Integer, String
from database.database import Base
from sqlalchemy.orm import relationship
from models import recipe_tags

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    recipes = relationship("Recipe", secondary=recipe_tags, back_populates="tags")