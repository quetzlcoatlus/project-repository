import time

def cli_input_home():
    while True:
            match(input("Waiting for input: ").lower()):
                case "help":
                    print("help command entered")
                case "wizard":
                    print("wizard command entered")
                case "logout":
                    print("logout command entered")
                case "exit":
                    print("Received exit command, closing..")
                    break
                case "edit preferences":
                    print("edit preferences command entered")
                case "view preferences":
                    print("view preferences command entered")
                case _:
                    print("Unrecognized input")
                    continue


def cli_input_view_preferences():
    while True:
            match(input("Type exit to return to the home screen or edit preferences to jump to that screen immediately: ").lower()):
                # case "help":
                #     print("help command entered")
                case "exit":
                    print("Received exit command, returning to home")
                    time.sleep(2)
                    break
                case "edit preferences":
                    print("edit preferences command entered")
                case _:
                    print("Unrecognized input")
                    continue


def cli_input_edit_preferences():
    while True:
            match(input("Type exit to return to the home screen: ").lower()):
                # case "help":
                #     print("help command entered")
                case "exit":
                    print("Received exit command, returning to home")
                    time.sleep(2)
                    break

                case "edit genre":
                    print("edit genre command entered")
                case "edit release range":
                    print("edit release range command entered")
                case "edit number of players":
                    print("edit number of players command entered")
                case "edit length":
                    print("edit length command entered")

                case _:
                    print("Unrecognized input")
                    continue