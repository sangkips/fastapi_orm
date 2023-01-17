from typing import Optional
from pydantic import BaseModel


class QuestionBase(BaseModel):
    title: str
    body: str
    tag_id: Optional[int]
    vote_id: Optional[int]


class QuestionCreate(QuestionBase):
    title: str
    body: str


class QuestionEdit(BaseModel):
    title: str
    body: str


class QuestionInDB(QuestionBase):
    id: int

    class Config:
        orm_mode = True
