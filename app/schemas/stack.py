from pydantic import BaseModel

class TechStackCreate(BaseModel):
    tech_name: str



class TechStackResponse(BaseModel):
    message: str
