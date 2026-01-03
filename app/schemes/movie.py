from pydantic import BaseModel, Field


class CategoryOut(BaseModel):
    name: str

class RatingOut(BaseModel):
    name: str

class ListMovie(BaseModel):
    show_id: str
    title: str
    type: str
    release_year: int
    rating: RatingOut
    categories: list[CategoryOut]
    cast: str | None = None
    director: str | None = None
    date_added: str | None = None
    country: str | None = None
    duration: str | None = None
    description: str | None = None

    class Config:
        orm_mode = True


class MovieSearchFilters(BaseModel):
    query: str | None = Field(None, description="Search by movie title")
    type_: str | None = Field(None, alias="type", description="Movie or TV Show")
    category: str | None = None
    rating: str | None = None
    year: int | None = None
    country: str | None = None
    cast: str | None = None
    director: str | None = None
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Movies per page")