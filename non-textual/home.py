import sys

import cli_functions

def print_home_banner(username: str, APP_TITLE: str) -> None:
    print(f"Welcome {username} to {APP_TITLE}!")
    print(f"Here you can generate recommendations, view, or edit preferences.")
    print(f"Type help to see commands you can use.")
    print()
    print(f"FYI: Your changes are associated with the account you logged in as.")
    print(f"If you have to quit the app, anything you changed persists!")
    print()
    print(f"If you're a new user, type the wizard command to take you through\npreference setup and your first generation!")


def home_sequence(username: str, APP_TITLE: str):
    print_home_banner(username, APP_TITLE)

    cli_functions.cli_input_home()


if __name__ == "__main__":
    sys.exit(print_home_banner("test", "Game Recommender"))