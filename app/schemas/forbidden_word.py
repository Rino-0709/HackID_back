from pydantic import BaseModel

class ForbiddenWordCreate(BaseModel):
    word: str

class ForbiddenWordResponse(BaseModel):
    message: str
