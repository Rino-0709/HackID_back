from pydantic import BaseModel

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    study_group: str

class UserResponse(BaseModel):
    id_telegram: int
    first_name: str
    last_name: str
    study_group: str
    tag_telegram: str
    role: int

    class Config:
        orm_mode = True
