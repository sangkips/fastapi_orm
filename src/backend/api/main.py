from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.db.database import engine, Base
from api.routers import answer, question, tag, user, vote, login

Base.metadata.create_all(bind=engine)


app = FastAPI(title="QuizBox")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(login.router, prefix="/login", tags=["Login"])
app.include_router(tag.router, prefix="/tags", tags=["Tags"])
app.include_router(answer.router, prefix="/answers", tags=["Answers"])
app.include_router(question.router, prefix="/questions", tags=["Questions"])
app.include_router(vote.router, prefix="/votes", tags=["Votes"])
