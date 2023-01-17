from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from api.models.answers import Answer
from api.schema._answer import AnswerCreate, AnswerEdit


def get_answer(db: Session, answer_id: int):
    return db.query(Answer).filter(Answer.id == answer_id).first()


def get_answers(db: Session):
    return db.query(Answer).all()


def create_answer(db: Session, answer: AnswerCreate):
    db_answer = Answer(
        body=answer.body,
        user_id=answer.user_id,
        vote_id=answer.vote_id,
        question_id=answer.question_id,
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def get_user_answers(db: Session, user_id: int):
    return db.query(Answer).filter(Answer.user_id == user_id).all()


def update_given_answer(db: Session, answer_id: int, answer: AnswerEdit):
    given_answer = db.query(Answer).filter(Answer.id == answer_id)
    if given_answer.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Answer with id {answer_id} not found")

    given_answer.update(jsonable_encoder(answer))
    db.commit()
    return {"message": "Answer updated successfully"}


def delete_given_answer(answer_id: int, db: Session):
    given_answer = db.query(Answer).filter(Answer.id == answer_id)
    if given_answer.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Answer with id {answer_id} not found")
    given_answer.delete(synchronize_session=False)
    db.commit()
    return {"message": "Answer deleted successfully"}
