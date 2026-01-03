from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.schemes.movie import ListMovie, MovieSearchFilters
from app.services.movieservice import MovieService
from db.models import Movie

router = APIRouter(
    dependencies=[Depends(get_current_user)],
)


@router.get('/list', response_model=list[ListMovie])
def list_movies(db: Session = Depends(get_db)):
    return MovieService(db).list_movies()


@router.get('/search', response_model=list[ListMovie])
def search_movies(
    filters: MovieSearchFilters = Depends(),
    db: Session = Depends(get_db),
):
    service = MovieService(db)
    movies = service.search_movie(filters)
    start = filters.page_size * (filters.page - 1)
    end = filters.page_size * filters.page
    return movies[start:end]