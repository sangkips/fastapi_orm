from pydantic import BaseModel


class AnswerBase(BaseModel):
    body: str
    vote_id: int | None = None
    question_id: int


class AnswerCreate(AnswerBase):
    ...


class AnswerEdit(BaseModel):
    body: str


class Answer(AnswerBase):
    id: int

    class Config:
        orm_mode = True
