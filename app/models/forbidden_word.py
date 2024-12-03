from sqlalchemy import Column, Integer, String
from app.database import Base

class ForbiddenWord(Base):
    __tablename__ = "forbidden_words"

    id_word = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word = Column(String, unique=True, nullable=False)
