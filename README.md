# My Movie Database

A command-line movie database application that allows you to manage your personal movie collection with data fetched from the OMDB API. The application stores movie information in a SQLite database and provides various features for organizing, analyzing, and displaying your movies.

## Features

- **Movie Management**
  - Add movies with automatic data fetching from OMDB API
  - Delete movies from your collection
  - Update movie ratings
  - List all movies with ratings and years

- **Search & Discovery**
  - Search movies with fuzzy matching
  - Get random movie suggestions
  - Sort movies by rating

- **Analytics**
  - View statistics (average, median, best/worst movies)
  - Generate rating histograms
  
- **Web Generation**
  - Generate a static HTML website to showcase your movie collection

## Requirements

- Python 3.7+
- SQLAlchemy
- requests
- matplotlib
- thefuzz
- python-dotenv

## Installation

1. Clone the repository or download the project files

2. Install required dependencies:
```bash
pip install sqlalchemy requests matplotlib thefuzz python-dotenv
```

3. Create a `.env` file in the project root and add your OMDB API key:
```
API_KEY=your_omdb_api_key_here
```

You can get a free API key from [OMDB API](http://www.omdbapi.com/apikey.aspx)

## Project Structure

```
.
├── movies.py                 # Main application file
├── movie_storage/
│   └── movie_storage_sql.py  # Database operations
├── _static/
│   ├── index_template.html   # HTML template for website generation
│   ├── style.css             # Stylesheet for generated website
│   └── index.html            # Generated website (created by app)
├── movies.db                 # SQLite database (created automatically)
└── .env                      # Environment variables (API key)
```

## Usage

Run the application:
```bash
python movies.py
```

### Menu Options

**0. Exit** - Exit the application

**1. List movies** - Display all movies in your database

**2. Add movie** - Add a new movie by title (fetches data from OMDB API)

**3. Delete movie** - Remove a movie from your collection

**4. Update movie** - Update a movie's rating (0-10)

**5. Stats** - View statistics about your movie collection

**6. Random movie** - Get a random movie suggestion

**7. Search movie** - Search for movies using keywords or fuzzy matching

**8. Movies sorted by rating** - Display movies sorted by rating (highest to lowest)

**9. Create rating histogram** - Generate a histogram visualization of movie ratings

**10. Generate website** - Create a static HTML website of your movie collection

## Database Schema

The application uses SQLite with the following table structure:

```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE NOT NULL,
    year INTEGER NOT NULL,
    rating REAL NOT NULL,
    poster_image_url TEXT NOT NULL
)
```

## Features in Detail

### Fuzzy Search
The search function uses fuzzy string matching to help find movies even with typos or partial matches. If an exact match isn't found, it will suggest similar movie titles.

### Statistics
The stats feature provides:
- Average rating across all movies
- Median rating
- Best rated movie
- Worst rated movie

### Website Generation
Generates a static HTML website displaying your movie collection with:
- Movie posters
- Titles
- Release years
- Responsive grid layout

## Error Handling

The application includes robust error handling for:
- Invalid user input
- API connection issues
- Missing movies
- Database errors

## Notes

- Movie titles must be unique in the database
- Ratings are stored as decimal values (0.0 - 10.0)
- The OMDB API has rate limits on free tier accounts
- Generated histograms are saved as `movie_rating_histogram.png`

## License

This project is provided as-is for educational and personal use.

## Credits

- Movie data provided by [OMDB API](http://www.omdbapi.com/)
- Fuzzy string matching powered by [thefuzz](https://github.com/seatgeek/thefuzz)