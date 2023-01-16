
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from sqlalchemy.orm import Session


from api.schema._question import QuestionCreate, Question, QuestionEdit
from api.utils.question_crud import get_question, get_questions, create_question
from api.db.database import get_db

router = APIRouter()


@router.get(
    "/",
    response_model=list[Question],
    status_code=status.HTTP_200_OK,
)
async def get_all_questions(db: Session = Depends(get_db)):
    questions = get_questions(db=db)
    return questions


@router.get("/{question_id}")
async def get_single_question(question_id: int, db: Session = Depends(get_db)):
    question = get_question(db=db, question_id=question_id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )
    return question


@router.post(
    "/",
    response_model=Question,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_question(question: QuestionCreate, db: Session = Depends(get_db)):
    new_question = create_question(db=db, question=question)
    return new_question


@router.patch("/{question_id}")
async def update_question(question: QuestionEdit, db: Session = Depends(get_db)):
    question_to_update = Question(db, question)
    if question_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question does not exist"
        )
    return question_to_update


@router.delete(
    "/{question_id}",
)
async def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = get_question(db, question_id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question does not exist"
        )
    db.delete(question)
    db.commit()

    return {"message": "Successfully deleted the question"}
