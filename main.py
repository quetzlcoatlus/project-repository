import sys
import os
import time

import home, login

APP_TITLE = "Game Recommender"

def clear_screen():
    os.system("clear")


# Login screen on startup

def print_startup_banner():
    print(f"Welcome to {APP_TITLE}!")
    print(f"Recommends games based on user preferences.")


def main():
    clear_screen()
    print_startup_banner()

    username = login.login_sequence()

    time.sleep(2)

    clear_screen()
    
    home.home_sequence(username, APP_TITLE)
    


    
    
if __name__ == "__main__":
    sys.exit(main())