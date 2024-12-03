from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "registered_users"

    id_telegram = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    study_group = Column(String, nullable=False)
    tag_telegram = Column(String, unique=True, nullable=False)
    role = Column(Integer, nullable=False)
