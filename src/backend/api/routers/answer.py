from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from sqlalchemy.orm import Session


from api.schema._answer import AnswerCreate, Answer, AnswerEdit
from api.utils.answer_crud import (
    get_answer,
    get_answers,
    create_answer,
    update_given_answer,
    delete_given_answer,
)
from api.db.database import get_db
from api.routers.login import get_current_user
from api.models.users import User


router = APIRouter()


@router.get("/", response_model=List[Answer])
async def get_all_answers(db: Session = Depends(get_db)):
    answers = get_answers(db=db)
    return answers


@router.get("{answer_id}", response_model=Answer)
async def get_single_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = get_answer(db=db, answer_id=answer_id)
    if answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not in the database"
        )
    return answer


@router.post("/", response_model=Answer)
async def create_new_answer(
    answer: AnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_answer = create_answer(db=db, answer=answer, user_id=current_user.id)
    return new_answer


@router.put("{answer_id}")
async def update_answer(
    answer_id: int, answer: AnswerEdit, db: Session = Depends(get_db)
):
    answer_to_update = update_given_answer(db=db, answer_id=answer_id, answer=answer)
    if answer_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Answer with given id {answer_id} does not exist",
        )
    return {"message": "Answer updated successfully"}


@router.delete("/{answer_id}")
async def delete_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    answer = get_answer(db=db, answer_id=answer_id)
    if answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer does not exist"
        )
    if answer.user_id == current_user.id or current_user.is_superuser:
        delete_given_answer(db=db, answer_id=answer_id, user_id=current_user.id)

        return {"message": "Answer deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied"
    )
