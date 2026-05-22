from sqlalchemy import Column, String, JSON

from app.data.database.database import Base


class RecipeDB(Base):
    __tablename__ = "recipes"
    uuid = Column(String, primary_key = True)
    url = Column(String, unique = True, index = True, nullable = False)
    generated_recipe = Column(JSON, nullable=False)
    original_recipe = Column(JSON, nullable = False)
