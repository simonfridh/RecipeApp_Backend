from sqlalchemy import Column, String, JSON

from app.data.database.database import Base
from app.domain.models.recipe import Recipe


class RecipeDB(Base):
    __tablename__ = "recipes"
    uuid = Column(String, primary_key = True)
    url = Column(String, unique = True, index = True, nullable = False)
    recipe = Column(JSON, nullable=False)