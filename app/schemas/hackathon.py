from pydantic import BaseModel
from typing import List

class HackathonRegister(BaseModel):
    team_name: str
    captain_tag: str
    role_in_team: str
    hackathon_id: int
    technology_stack: List[int]

class HackathonRegisterResponse(BaseModel):
    message: str

class MessageResponse(BaseModel):
    message: str

class ActiveHackathonCreate(BaseModel):
    hackathon_name: str
    host_hackathon: str
    activity_status: int

class ActiveHackathonResponse(BaseModel):
    message: str

class HackathonResponse(BaseModel):
    hackathon_id: int
    hackathon_name: str
    host_hackathon: str
    activity_status: int

    class Config:
        orm_mode = True  # Позволяет работать с SQLAlchemy моделями

class QuestionnaireResponse(BaseModel):
    team_name: str

    class Config:
        orm_mode = True  # Позволяет работать с SQLAlchemy моделями

class TeamMemberResponse(BaseModel):
    telegram_tag: str
    first_name: str
    last_name: str
    group: str
    team_name: str
    captain_tag: str
    role_in_team: str
    technology_stack: List[str]

    class Config:
        orm_mode = True  # Позволяет работать с SQLAlchemy моделями