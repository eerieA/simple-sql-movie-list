import datetime
import database

# ============================================================================ #
# Constants

menu = """Please select what to do:
1) Add new movie
2) View upcoming movies
3) View all movies
4) Watch a movie
5) View watched movies
6) Add user
7) Search for a movie
8) Exit.

Your selection: """


# ============================================================================ #
# Initializing

welcome = "Welcome to this movie watchlist app!"
print(welcome)
database.create_tables()


# ============================================================================ #
# Functions

def prompt_add_movie():
    title = input("Movie title: ")
    release_date = input("Release date (dd-mm-yyyy): ")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()

    database.add_movie(title, timestamp)


def print_movie_list(heading, movies):
    print(f"\\\ {heading} movies //")
    for movie in movies:
        # [0] is the id, [1] is the title, [2] is the timestamp
        movie_date = datetime.datetime.fromtimestamp(movie[2])
        human_movie_date = movie_date.strftime("%b %d %Y")
        print(f"{movie[0]}: {movie[1]} (on {human_movie_date})")
    print("------ \n")


def prompt_watch_movie():
    username = input("Username: ")
    movie_id = input("Enter ID of the movie you have watched: ")
    database.watch_movie(username, movie_id)


def prompt_add_user():
    username = input("Username: ")
    database.add_user(username)


def promt_print_watched_movies():
    username = input("Username: ")
    movies = database.get_watched_movies(username)
    if movies:
        print_movie_list(f"{username}'s watched", movies)
    else:
        print("This user has not watched any movies yet.")


def prompt_search_movies():
    search_term = input("Enter a search keyword: ")
    movies = database.search_movies(search_term)
    if movies:
        print_movie_list("Movies found", movies)
    else:
        print("Sorry, no movies found for that keyword.")


# ============================================================================ #
# Menu UI

while (user_input := input(menu)) != "8":
    if user_input == "1":
        prompt_add_movie()
    elif user_input == "2":
        movies = database.get_movies(True)
        print_movie_list("Upcoming", movies)
    elif user_input == "3":
        movies = database.get_movies()
        print_movie_list("All", movies)
    elif user_input == "4":
        prompt_watch_movie()
    elif user_input == "5":
        promt_print_watched_movies()
    elif user_input == "6":
        prompt_add_user()
    elif user_input == "7":
        prompt_search_movies()
    else:
        print("Invalid choice. Please try again!")