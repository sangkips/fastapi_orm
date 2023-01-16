import fastapi

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from sqlalchemy.orm import Session

from api.schema._vote import VoteCreate, Vote
from api.utils.vote_crud import (
    get_vote,
    get_votes,
    create_vote,
)
from api.db.database import get_db

router = APIRouter()


@router.get("/", response_model=List[Vote])
async def get_all_votes(db: Session = Depends(get_db)):
    return get_votes(db=db)


@router.get(
    "/{vote_id}",
    response_model=Vote,
    status_code=status.HTTP_200_OK,
)
async def get_single_vote(vote_id: int, db: Session = Depends(get_db)):
    return get_vote(db=db, vote_id=vote_id)


@router.post(
    "/",
    response_model=Vote,
    status_code=status.HTTP_201_CREATED,
)
async def create_vote_record(vote: VoteCreate, db: Session = Depends(get_db)):
    return create_vote(db=db, vote=vote)


@router.put("/{vote_id}")
async def update_vote():
    pass


@router.delete("/{vote_id}")
async def delete_vote(vote_id: int, db: Session = Depends(get_db)):
    vote = get_vote(db, vote_id)

    db.delete(vote)
    db.commit()
    db.refresh(vote)

    return {"message": " Delete successful"}
