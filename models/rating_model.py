from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from database.database import Base
from sqlalchemy.orm import relationship

class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (UniqueConstraint("user_id", "recipe_id", name="user_recipe_uc"),)

    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="ratings")
    recipe = relationship("Recipe", back_populates="ratings")