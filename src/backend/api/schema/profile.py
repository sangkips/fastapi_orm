from pydantic import BaseModel


class UserProfile(BaseModel):
    first_name: str
    last_name: str
    bio: str

    class Config():
        orm_mode = True
