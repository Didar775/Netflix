from fastapi import FastAPI
from sqlalchemy.orm import Session
from db.models import Base, Movie
from db.base import engine, SessionLocal
from .routers import auth, users, movies
from contextlib import asynccontextmanager
from .services.upload_csv import upload_csv


@asynccontextmanager
async def lifespan(app: FastAPI):
    db: Session = SessionLocal()
    movie_count = db.query(Movie).count()
    if movie_count == 0:
        upload_csv(db)
    yield


app = FastAPI(lifespan=lifespan)

Base.metadata.create_all(bind=engine)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

app.include_router(movies.router, prefix="/movies", tags=["movies"])