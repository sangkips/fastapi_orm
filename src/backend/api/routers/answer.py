from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from sqlalchemy.orm import Session


from api.schema._answer import AnswerCreate, Answer
from api.utils.answer_crud import get_answer, get_answers, create_answer
from api.db.database import get_db


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
async def create_new_answer(answer: AnswerCreate, db: Session = Depends(get_db)):
    new_answer = create_answer(db=db, answer=answer)
    return new_answer


"""  
@router.put("{answer_id}")
async def update_answer():
    pass
"""


@router.delete("/{answer_id}", response_model=Answer)
async def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = get_answer(db, answer_id)
    if answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer does not exist"
        )
    db.delete(answer)
    db.commit()
    db.refresh(answer)
    return {"Detail": "Deletion successfull"}
