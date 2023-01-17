from fastapi import APIRouter, Depends, HTTPException, status
from typing import List


from sqlalchemy.orm import Session


from api.schema._question import QuestionCreate, QuestionEdit, QuestionInDB
from api.utils.question_crud import (
    get_question,
    get_questions,
    create_question,
    update_given_question,
)
from api.db.database import get_db
from api.models.users import User
from api.routers.login import get_current_user


router = APIRouter()


@router.get(
    "/",
    response_model=list[QuestionInDB],
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
    response_model=QuestionInDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_question = create_question(db=db, question=question, user_id=current_user.id)
    return new_question


@router.put("/{question_id}")
async def update_question(
    question_id: int, question: QuestionEdit, db: Session = Depends(get_db)
):

    question_updated = update_given_question(
        question_id=question_id, question=question, db=db
    )
    if question_updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id {question_id} not found",
        )
    return question_updated


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
