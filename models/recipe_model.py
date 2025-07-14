from sqlalchemy import Column, Integer, String, Text, Float
from database.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    ingredients = Column(Text)
    steps = Column(Text)
    image = Column(String)
    average_rating = Column(Float, default=0.0)
