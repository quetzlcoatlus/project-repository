# Can be replaced with a database later

VALID_USERS = {
    "test": "1234"
}


def authenticated(username: str, password: str) -> bool:
    if username not in VALID_USERS:
        print("Username not found in valid users.")
        return False

    if password != VALID_USERS[username]:
        print("Wrong password for user.")
        return False
    
    print(f"Successfully authenticated as {username}!")
    return True


def login_sequence() -> str:
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if authenticated(username, password):
            break

    return username