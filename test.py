

VALID_USERS = {
    "test": "1234"
}

print(VALID_USERS["test"])

username = 'test'
password = '1234'

print(password is not VALID_USERS[username])