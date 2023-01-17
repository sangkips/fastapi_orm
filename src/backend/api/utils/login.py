from sqlalchemy.orm import Session

from api.models.users import User


def get_user(username: str, db: Session):
    user = db.query(User).filter(User.email == username).first()
    return user
