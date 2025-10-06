"""
A basic module for managing a SQLite database of movies.

This module provides functionality to retrieve, add, delete, and update
movies in the database. Each movie is stored with a title, year, and
rating attribute. The SQLite database is created and managed via SQLAlchemy.
"""
from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=False)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
                            CREATE TABLE IF NOT EXISTS movies
                            (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT UNIQUE NOT NULL,
                                year INTEGER NOT NULL,
                                rating REAL NOT NULL,
                                poster_image_url TEXT NOT NULL
                            )
                            """))
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("""SELECT
                                                title,
                                                year,
                                                rating,
                                                poster_image_url
                                            FROM movies"""))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "image": row[3]} for row in movies}


def add_movie(title, year, rating, image):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("""INSERT INTO movies (title, year, rating, poster_image_url)
                                       VALUES (:title, :year, :rating, :image)"""),
                               {"title": title, "year": year, "rating": rating, "image": image})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("""DELETE
                                       FROM movies
                                       WHERE title = :title"""),
                               {"title": title})
            connection.commit()
            print(f"Movie '{title}' deleted successfully")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("""UPDATE movies
                                       SET rating = :rating
                                       WHERE title = :title"""),
                               {"title": title, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' updated successfully")
        except Exception as e:
            print(f"Error: {e}")
