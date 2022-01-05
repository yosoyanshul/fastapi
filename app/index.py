from fastapi import FastAPI
import psycopg2
from .database import engine
from . import models
from .routers import posts, users, auth, vote




models.Base.metadata.create_all(bind=engine)
app = FastAPI()



@app.get("/")
def root():
    return {"Up and Running"}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)