# Generates screen with list of <user> preferences

# Might substitute with a database at some point, for now it can be a dictionary

# Holds values for preferences:
# Genres can be a list of strings
# Release range will be a size 2 tuple
# Number of players is an integer
# Length is an integer representing hours

test_preferences = {
    'genres': ['action', 'horror', 'shooter'],
    'release_range': (2000, 2008),
    'number_of_players': 1,
    'length': 5
}

def print_edit_preferences_banner():
    print(f"Preferences determine how the recommender decides what to recommend")
    print(f"Type edit folowed by the name of the preference (e.g. genre) to go to a screen to add or remove preferences.")


def edit_preferences_view():
    print_edit_preferences_banner()


def print_view_preferences_banner():
    print(f"Preferences determine how the recommender decides what to recommend")


def view_preferences_view():
    print_view_preferences_banner()

