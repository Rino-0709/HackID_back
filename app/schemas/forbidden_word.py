from pydantic import BaseModel

class ForbiddenWordCreate(BaseModel):
    word: str

class ForbiddenWordResponse(BaseModel):
    message: str

class ForbiddenWordGetResponse(BaseModel):
    id: int
    word: str

    class Config:
        orm_mode = True