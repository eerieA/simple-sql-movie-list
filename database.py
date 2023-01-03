import os
import datetime
import psycopg2
from dotenv import load_dotenv

# ============================================================================ #
# Constants (SQL queries)

# This loads the .env under root by default
load_dotenv()

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);
"""
CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);
"""
CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users(username),    
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);
"""
INSERT_MOVIES = (
    "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"
)
INSERT_USER = (
    "INSERT INTO users (username) VALUES (%s);"
)
DELETE_MOVIE = "DELETE FROM movies WHERE title = %s;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"
SELECT_WATCHED_MOVIES = """SELECT * FROM movies
JOIN watched ON movies.id = watched.movie_id
JOIN users ON users.username = watched.user_username
WHERE users.username = %s;"""
INSERT_WATCHED_MOVIES = (
    "INSERT INTO watched (user_username, movie_id) VALUES (%s, %s);"
)
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = %s;"
SEARCH_MOVIES = "SELECT * FROM movies WHERE title LIKE %s;"
CREATE_RELEASE_INDEX = "CREATE INDEX IF NOT EXISTS idx_movies_release ON movies(release_timestamp);"


# ============================================================================ #
# Initializing

# This reads the variable named as the string in the .env. becasue .env was loaded before
# and environ is a dictionary so we have to pass in variable name inside quotes
connection = psycopg2.connect(os.environ["DATABASE_URL"])


# ============================================================================ #
# Functions

def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)
            # cursor.execute(CREATE_RELEASE_INDEX)


def add_movie(title, release_timestamp):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES, (title, release_timestamp))


def add_user(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))


def get_movies(upcoming=False):
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                today_timestamp = datetime.datetime.now().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()


def search_movies(search_term):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_MOVIES, (f"%{search_term}%",))
            return cursor.fetchall()


def watch_movie(username, movie_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WATCHED_MOVIES, (username, movie_id))


def get_watched_movies(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES, (username,))
            return cursor.fetchall()
