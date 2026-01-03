from sqlalchemy import String, ForeignKey, Integer, Text, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f'<User id={self.id} email={self.email}>'


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    token: Mapped[str] = mapped_column(nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")




movie_category = Table(
    "movie_category",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.show_id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)



class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)


class Rating(Base):
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)


class Movie(Base):
    __tablename__ = "movies"
    show_id: Mapped[str] = mapped_column(String, primary_key=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    release_year: Mapped[int] = mapped_column(Integer, nullable=True)

    rating_id: Mapped[int] = mapped_column(
        ForeignKey("ratings.id"),
        nullable=False,
    )

    rating: Mapped["Rating"] = relationship(lazy="joined")

    categories: Mapped[list["Category"]] = relationship(
        secondary=movie_category,
        backref="movies",
        lazy="joined",
    )

    description: Mapped[str]
    director: Mapped[str]
    cast: Mapped[str]
    country: Mapped[str]
    duration: Mapped[str]
    date_added: Mapped[str]