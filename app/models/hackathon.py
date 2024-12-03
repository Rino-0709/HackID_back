from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY
from app.database import Base

class SubmittedQuestionnaire(Base):
    __tablename__ = "submitted_questionnaires"

    hackathon_id = Column(Integer, nullable=False)
    id_telegram = Column(Integer, primary_key=True, index=True)
    captain_tag = Column(String, nullable=False)
    participant_role = Column(String, nullable=False)
    stack_list = Column(ARRAY(Integer), nullable=False)
    team_name = Column(String, nullable=False)

class Hackathon(Base):
    __tablename__ = 'active_hackathons'

    hackathon_id = Column(Integer, primary_key=True, autoincrement=True)  # Автоинкремент
    hackathon_name = Column(String, nullable=False)
    host_hackathon = Column(String, nullable=False)
    activity_status = Column(Integer, nullable=False)

