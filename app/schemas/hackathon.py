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
