from pydantic import BaseModel


class QuestionBase(BaseModel):
    title: str
    body: str
    user_id: int
    tag_id: int
    vote_id: int | None = None


class QuestionCreate(QuestionBase):
    ...


class QuestionEdit(BaseModel):
    title: str
    body: str


class QuestionInDB(QuestionBase):
    id: int

    class Config:
        orm_mode = True
