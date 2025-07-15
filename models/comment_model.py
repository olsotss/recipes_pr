from sqlalchemy import Column, ForeignKey, Integer, Text
from database.database import Base
from sqlalchemy.orm import relationship

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="comments")
    recipe = relationship("Recipe", back_populates="comments")