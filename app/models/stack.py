from sqlalchemy import Column, Integer, String
from app.database import Base

class TechStack(Base):
    __tablename__ = "stack_table"

    technology_id = Column(Integer, primary_key=True, index=True)
    technology_name = Column(String, unique=True, nullable=False)

