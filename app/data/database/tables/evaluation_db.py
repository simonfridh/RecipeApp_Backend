from sqlalchemy import Column, String, JSON

from app.data.database.database import Base


class EvaluationDb(Base):
    __tablename__ = "evaluations"
    uuid = Column(String, primary_key = True)
    url = Column(String, unique = True, index = True, nullable = False)
    evaluation = Column(JSON, nullable=False)