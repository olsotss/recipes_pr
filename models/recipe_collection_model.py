from sqlalchemy import Column, Integer,ForeignKey, Table
from database.database import Base

collection_recipes = Table(
    "collection_recipes",
    Base.metadata,
    Column("collection_id", Integer, ForeignKey("collections.id", ondelete="CASCADE")),
    Column("recipe_id", Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
)
