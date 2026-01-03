from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.schemes.movie import MovieSearchFilters
from db.models import Movie, Rating, Category


class MovieService:
    def __init__(self, db: Session):
        self.db = db

    def list_movies(self):
        stmt = (
            select(Movie)
            .options(
                selectinload(Movie.categories),  # load categories efficiently
                selectinload(Movie.rating)  # load rating efficiently
            )
        )
        return self.db.execute(stmt).scalars().all()

    def search_movie(self, filters: MovieSearchFilters) -> list[Movie]:
        stmt = select(Movie).options(
            selectinload(Movie.categories),
            selectinload(Movie.rating)
        )

        # Apply filters from MovieSearchFilters
        if filters.query:
            stmt = stmt.where(Movie.title.ilike(f"%{filters.query}%"))
        if filters.type_:
            stmt = stmt.where(Movie.type == filters.type_)
        if filters.year:
            stmt = stmt.where(Movie.release_year == filters.year)
        if filters.rating:
            stmt = stmt.join(Movie.rating).where(Rating.name == filters.rating)
        if filters.category:
            stmt = stmt.join(Movie.categories).where(Category.name.ilike(f"%{filters.category}%"))
        if filters.country:
            stmt = stmt.where(Movie.country.ilike(f"%{filters.country}%"))

        return list(self.db.execute(stmt).unique().scalars().all())
