from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from sqlalchemy.orm import Session

from api.models.users import User
from api.schema._question import QuestionInDB
from api.schema._user import UserCreate, UserInDB
from api.utils.user_crud import (
    get_user,
    get_user_by_email,
    get_users,
    create_user,
)
from api.utils.question_crud import get_user_questions
from api.db.database import get_db
from api.schema.profile import UserProfile


router = APIRouter()

# get all users from the database(100 records at a time)


@router.get("/", response_model=List[UserInDB])
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


# get a single user by id
@router.get("/{user_id}", response_model=UserInDB)
async def get_single_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    return user


# get queations beloging to a given user
@router.get("/{user_id}/questions", response_model=List[QuestionInDB])
async def get_questions_for_given_user(user_id: int, db: Session = Depends(get_db)):
    questions = get_user_questions(user_id=user_id, db=db)
    return questions


# create a new user
@router.post(
    "/",
    response_model=UserInDB,
    status_code=status.HTTP_201_CREATED,
)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = get_user_by_email(db=db, email=user.email)
    if new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with email already exist.",
        )
    return create_user(db=db, user=user)


# update user based on a given username
@router.put("{username}", response_model=UserProfile)
async def update_user(username: str, user: UserProfile, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.bio = user.bio
    db.add(db_user)
    db.refresh(db_user)
    db.commit()
    return {
        "username": db_user.username,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "bio": db_user.bio,
    }


# delete user


@router.delete(
    "{user_id}",
)
async def delete_current_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    db.delete(user)
    db.commit()

    return {"message": "Successfully deleted the user"}
