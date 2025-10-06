"""
A program to manage a movie database, allowing adding, deleting, updating,
sorting, and creating statistics related to movies in the database.

The module provides various functions to interact with the movie database:
- listing movies
- adding new movies
- deleting existing ones
- updating their details
- retrieving statistics
- generating a random movie suggestion
- searching for movies
- sorting by ratings
- producing a histogram of ratings
"""
import os
import random
import sys

import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv
from thefuzz import process, fuzz

from movie_storage import movie_storage_sql as storage

load_dotenv()
API_KEY = os.getenv('API_KEY')

# Colors
COLORS = {
    'header': '\033[95m',
    'blue': '\033[94m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'warning': '\033[93m',
    'fail': '\033[91m',
    'endc': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m'
}


# Features of the movie application
def list_movies():
    """List of all movies in the movie database."""

    # Get the data from the SQL database
    movies = storage.list_movies()

    print(f"{len(movies)} in total")
    for movie in movies:
        print(f"{movie} ({movies[movie]['year']}): {movies[movie]['rating']}")


def add_movie():
    """Adds a new movie to the movie database."""

    # Get the data from the SQL database
    movies = storage.list_movies()

    while True:
        title = input(COLORS['warning'] + "Enter new movie name: " + COLORS['endc'])
        if title == "":
            print(COLORS['fail'] + "Please enter a movie name" + COLORS['endc'])
        else:
            break

    if title not in movies:

        try:
            url = f'https://www.omdbapi.com/?apikey={API_KEY}&t={title}'
            res = requests.get(url, timeout=10)

            data = res.json()

            if data['Title'] not in movies:

                # Add the movie and save the data to the SQL database
                storage.add_movie(data['Title'],
                                  int(data['Year']),
                                  float(data['imdbRating']),
                                  data['Poster'])

            else:
                print(COLORS['fail'] + f"Movie {title} already exist!" + COLORS['endc'])

        except KeyError:
            print(COLORS['fail'] + f"Movie {title} not found" + COLORS['endc'])

        except requests.exceptions.ConnectionError:
            print(COLORS['fail'] +
                  "Could not connect to the API. Please check your internet connection." +
                  COLORS['endc'])

        except requests.exceptions.Timeout:
            print(COLORS['fail'] + "The request timed out. Please try again." + COLORS['endc'])

    else:
        print(COLORS['fail'] + f"Movie {title} already exist!" + COLORS['endc'])


def delete_movie():
    """Deletes a movie from the movie database."""

    # Get the data from the SQL database
    movies = storage.list_movies()

    while True:
        title = input(COLORS['warning'] + "Enter movie name to delete: " + COLORS['endc'])
        if title == "":
            print(COLORS['fail'] + "Please enter a movie name" + COLORS['endc'])
        else:
            break

    if title in movies:
        storage.delete_movie(title)
    else:
        print(COLORS['fail'] + f"Movie {title} doesn't exist!" + COLORS['endc'])


def update_movie():
    """Updates a movie from the movies database."""

    # Get the data from the SQL database
    movies = storage.list_movies()

    while True:
        title = input(COLORS['warning'] + "Enter movie name: " + COLORS['endc'])
        if title == "":
            print(COLORS['fail'] + "Please enter a movie name" + COLORS['endc'])
        else:
            break

    if title in movies:

        while True:
            try:
                rating = float(input(COLORS['warning'] +
                                     "Enter new movie rating (0-10): "
                                     + COLORS['endc']))
                if 0 <= rating <= 10:
                    movies[title]['rating'] = rating
                    break
                print(COLORS['fail'] + "Please enter a valid number." + COLORS['endc'])
            except ValueError:
                print(COLORS['fail'] + "Please enter a valid number." + COLORS['endc'])

        # Update the movie in the SQL database
        storage.update_movie(title, rating)

    else:
        print(COLORS['fail'] + f"Movie {title} not found" + COLORS['endc'])


def stats():
    """Shows statistics about the movies database."""

    # Get the data from the SQL database
    movies = storage.list_movies()

    ratings = [movies[movie]["rating"] for movie in movies]

    # Average
    average = sum(ratings) / len(ratings)
    print(f"Average rating: {round(average, 1)}")

    # Median
    sorted_ratings = sorted(ratings)
    mid = int(len(sorted_ratings) / 2)

    if len(sorted_ratings) % 2 != 0:
        median = sorted_ratings[mid]
    else:
        median = (sorted_ratings[mid - 1] + sorted_ratings[mid]) / 2

    print(f"Median rating: {median}")

    # Best and worst movie
    maximum = max(ratings)
    minimum = min(ratings)
    for movie in movies:
        if movies[movie]["rating"] == maximum:
            print(f"Best movie: {movie} ({movies[movie]["year"]}), {movies[movie]["rating"]}")
        if movies[movie]["rating"] == minimum:
            print(f"Worst movie: {movie} ({movies[movie]["year"]}), {movies[movie]["rating"]}")


def random_movie():
    """Gives a random movie from the movie database."""

    # Get the data from the SQL database
    movies = storage.list_movies()

    movie, values = random.choice(list(movies.items()))
    print(f"Your movie for tonight: {movie}, it's rated {values['rating']}")


def search_movie():
    """Search for a movie in the movies database."""

    # Get the data from the SQL database
    movies = storage.list_movies()

    while True:
        title = input(COLORS['warning'] + "Enter part of movie name: " + COLORS['endc'])
        if title == "":
            print(COLORS['fail'] + "Please enter a movie name" + COLORS['endc'])
        else:
            break

    movie_is_found = False

    # First search with keyword matching
    for movie in movies:
        if title.lower() in movie.lower():
            print(f"{movie} ({movies[movie]['year']}): {movies[movie]['rating']}")
            movie_is_found = True

    # Second search with fuzzy string matching
    if not movie_is_found:
        fuzzy_search = process.extract(title, movies.keys(), scorer=fuzz.token_set_ratio)

        # Error if the first result has a low score (< 53)
        if fuzzy_search[0][1] < 53:
            print(COLORS['fail'] + f"Movie {title} not found!" + COLORS['endc'])

        # Found results with a high score (>= 53)
        else:
            print(f'The movie "{title}" does not exist. Did you mean:')
            for fuzzy_movie, score in fuzzy_search:
                if score >= 53:
                    print(f"{fuzzy_movie} ({movies[fuzzy_movie]['year']}), "
                          f"{movies[fuzzy_movie]['rating']}")


def movies_sorted_by_rating():
    """Sort movies by rating."""

    # Get the data from the SQL database
    movies = storage.list_movies()

    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    for movie in sorted_movies:
        print(f"{movie[0]} ({movie[1]['year']}): {movie[1]['rating']}")


def create_rating_histogram():
    """Creates a histogram of rating values."""

    # Get the data from the SQL database
    movies = storage.list_movies()

    # Generate data for the histogram
    data = [movie["rating"] for movie in movies.values()]

    # Plotting a histogram
    plt.hist(data, color='skyblue', edgecolor='black')

    # Adding labels and title
    plt.xlabel('Ratings')
    plt.ylabel('Movies per Rating')
    plt.title('Movie Ratings Histogram')

    # Display the plot
    plt.savefig("movie_rating_histogram.png")
    plt.close()


def exit_database():
    """
    Exits the database application and terminates the program.
    """
    print("Bye!")
    sys.exit(0)


def serialize_movie(title, infos):
    """Serializes a movie object into a string."""

    output = ''

    output += '<li>'
    output += '<div class="movie">'
    output += ('<img class="movie-poster"'
               f'src="{infos["image"]}">')
    output += f'<div class="movie-title">{title}</div>'
    output += f'<div class="movie-year">{infos["year"]}</div>'
    output += '</div>'
    output += '</li>'

    return output


def create_movies_html(movies_data):
    """
    Generates HTML markup for a collection of movies.
    """

    output = ""

    if movies_data:
        for title, infos in movies_data.items():
            output += serialize_movie(title, infos)

    else:
        output = "<h2>There is no movie at the moment</h2>"

    return output


def generate_website():
    """
    Generates a static HTML website for displaying a list of movies.
    """

    # Get the data from the SQL database
    movies = storage.list_movies()

    with open('_static/index_template.html', 'r', encoding="utf-8") as file:
        template = file.read()

    template = template.replace("__TEMPLATE_TITLE__", "My Movie App")
    template = template.replace("__TEMPLATE_MOVIE_GRID__", create_movies_html(movies))

    with open('_static/index.html', 'w', encoding="utf-8") as file:
        file.write(template)

    print("Website was generated successfully.")


# Main function
def main():
    """
    Main function to handle interactions with the Movies Database.
    """
    print("********** My Movies Database **********")
    while True:

        # Show menu
        print(COLORS['header'] + "\n"
                                 "Menu:"
                                 "\n0. Exit"
                                 "\n1. List movies"
                                 "\n2. Add movie"
                                 "\n3. Delete movie"
                                 "\n4. Update movie"
                                 "\n5. Stats"
                                 "\n6. Random movie"
                                 "\n7. Search movie"
                                 "\n8. Movies sorted by rating"
                                 "\n9. Create rating histogram"
                                 "\n10. Generate website"
                                 "\n" + COLORS['endc']
              )

        # Select choice
        choices = {
            "0": exit_database,
            "1": list_movies,
            "2": add_movie,
            "3": delete_movie,
            "4": update_movie,
            "5": stats,
            "6": random_movie,
            "7": search_movie,
            "8": movies_sorted_by_rating,
            "9": create_rating_histogram,
            "10": generate_website
        }
        choice = input(COLORS['warning'] + "Enter your choice (0-10): " + COLORS['endc'])

        if choice in choices:
            print()  # Linebreak
            choices[choice]()
            input(COLORS['underline'] + "\nPress enter to continue" + COLORS['endc'])
        else:
            print(COLORS['fail'] + "Invalid choice" + COLORS['endc'])


if __name__ == "__main__":
    main()
