from sqlalchemy.orm import Session

from api.models.questions import Question
from api.schema._question import QuestionCreate


def get_question(db: Session, question_id: int):
    question_query = db.query(Question).filter(
        Question.id == question_id).first()
    return question_query


def get_questions(db: Session):
    return db.query(Question).all()


def create_question(db: Session, question: QuestionCreate):
    db_question = Question(
        title=question.title,
        body=question.body,
        user_id=question.user_id,
        tag_id=question.tag_id,
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_user_questions(db: Session, user_id: int):
    return db.query(Question).filter(Question.user_id == user_id).all()