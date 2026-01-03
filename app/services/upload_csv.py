import pandas as pd
from db.models import Rating, Category, Movie


def upload_csv(db):
    csv_file = 'app/services/netflix.csv'
    df = pd.read_csv(csv_file)

    rating_cache: dict[str, Rating] = {}
    category_cache: dict[str, Category] = {}


    for _, row in df.iterrows():
        rating_name = str(row["rating"]).strip() or "UNKNOWN"

        rating = rating_cache.get(rating_name)

        if not rating:
            rating = db.query(Rating).filter_by(name=rating_name).first()
            if not rating:
                rating = Rating(name=rating_name)
                db.add(rating)
                db.flush()
            rating_cache[rating_name] = rating

        categories = []

        for cat_name in str(row["listed_in"]).split(", "):
            cat_name = cat_name.strip()
            if not cat_name:
                continue

            category = category_cache.get(cat_name)
            if not category:
                category = db.query(Category).filter_by(name=cat_name).first()
                if not category:
                    category = Category(name=cat_name)
                    db.add(category)
                    db.flush()
                category_cache[cat_name] = category

            categories.append(category)

        movie = Movie(
            show_id=str(row["show_id"]),
            type=row["type"],
            title=row["title"],
            rating=rating,
            categories=categories,
            release_year=int(row["release_year"]),
            cast=row["cast"],
            director=row["director"],
            description=row["description"],
            date_added=row["date_added"],
            duration=row["duration"],
            country=row["country"],
        )

        db.add(movie)

    db.commit()