# Functionality for the list of genres view

genre_options = [
    'Action',
    'Adventure',
    'Puzzle',
    'Role-playing',
    'Simulation',
    'Strategy',
    'Sports',
    'MMO'
]

def print_list_of_genres_banner():
    print(f"Genre preferences limit what the recommender will select from.")
    print(f"Type add/delete followed by name of the genre to add or remove a particular genre as a preference.")
    print(f"Type genre options to see a list of options.")


def print_genre_options():
    print(f"Genre options:")
    for genre in genre_options:
        print(f"{genre}")

