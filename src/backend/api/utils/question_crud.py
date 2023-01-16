from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from api.models.questions import Question
from api.schema._question import QuestionCreate, QuestionEdit


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


def update_given_question(question_id: int, question: QuestionEdit, db: Session):
    question_to_update = db.query(Question).filter(Question.id == question_id)
    if not question_to_update.first():
        return f"Question with id {question_id} does not exist"

    question_to_update.update(jsonable_encoder(question))
    db.commit()
    return {"message": "Question updated successfully"}
