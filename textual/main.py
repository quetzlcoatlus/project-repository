"""
Docstring for textual.main

Defines the main program implementation (Sprint 1)

Classes are screens which are popped and pushed off the view stack
"""

from dataclasses import dataclass

from time import sleep

from textual.app import App, ComposeResult
from textual.widgets import Header, Input, RichLog
from textual.screen import Screen
from textual.reactive import reactive

VALID_USERS = {
    "test": "1234"
}

def validate_credentials(username: str, password: str) -> bool:
    return username in VALID_USERS and password == VALID_USERS[username]


@dataclass
class AuthState:
    username: str = ""
    # is_authed: bool = False


@dataclass
class PreferenceState:
    prefs = {
        "genres": [],
        "release_range": (2000, 2005),
        "number_of_players": 1,
        "length": 5,
    }


class BaseCLIScreen(Screen):
    """Screen with RichLog + Input, CLI-style"""

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(id="log")
        yield Input(id="cmd")

    def on_mount(self) -> None:
        self.query_one("#cmd", Input).focus()
        self.query_one("HeaderIcon").visible = False

    def _log(self, text: str) -> None:
        self.query_one("#log", RichLog).write(text)

    def clear_input(self) -> None:
        self.query_one("#cmd", Input).value = ""

    def get_app(self) -> "GameRecommenderApp":
       return self.app # type: ignore[return-value]


class LoginScreen(BaseCLIScreen):
    """Login screen with username and password prompt."""
    step: reactive[str] = reactive("username") # username -> password

    def on_mount(self) -> None:
        super().on_mount()
        app = self.get_app()
        self._log(f"Welcome to {app.TITLE}!")
        self._log("Recommends games based on user preferences.")
        self._log("")
        self._log("Log in with your credentials to begin.")
        self._log("Submit with Enter.")
        self._switch_to_username_mode()

    def _switch_to_username_mode(self) -> None:
        self.step = "username"
        inp = self.query_one("#cmd", Input)
        inp.password = False
        inp.placeholder = "Enter Username: "
        self.clear_input()

    def _switch_to_password_mode(self) -> None:
        self.step = "password"
        inp = self.query_one("#cmd", Input)
        inp.password = True
        inp.placeholder = "Enter Password: "
        self.clear_input()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        app = self.get_app()
        inp = event.input
        raw = inp.value.strip()

        if self.step == "username":
            if not raw:
                inp.focus()
                return
            app.auth.username = raw
            self._log(f"Attempting to login as {app.auth.username}...")
            self._switch_to_password_mode()

        elif self.step == "password":
            if not raw:
                inp.focus()
                return
            
            ok = validate_credentials(app.auth.username, raw)
            self.clear_input()

            if ok:
                # app.auth.is_authed = True
                self.app.pop_screen()
                self.app.push_screen(HomeScreen())
            else:
                self._log("Authentication failed, try again.")
                app.auth = AuthState()
                self._switch_to_username_mode()
            

class HomeScreen(BaseCLIScreen):
    """Home screen with command implementation, traverse to different views"""
    def on_mount(self) -> None:
        super().on_mount()
        app = self.get_app()
        self._log(f"{app.auth.username} welcome to Game Recommender!")
        self._log("Here you can generate your recommendations or view/edit preferences.")
        self._log("Type 'help' to see commands.")
        self._log("")
        self._log("Your changes are associated with your user if you quit the app.")
        self._log("")
        self._log("If you're a new user, type the 'quick start' command to have\ninstructions you can follow for preference setup and a generation\nprinted on the screen!")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        self.clear_input()
        if not raw:
            return
        
        cmd, *args = raw.split()
        await self._handle_commands(cmd, args)
        
    async def _handle_commands(self, cmd: str, args: list[str]) -> None:
        """Handles commands associated with the screen"""
        app = self.get_app()

        match cmd.lower():
            case "help":
                self.print_help_message()
            case "logout":
                app.auth = AuthState()
                app.pop_screen()
                app.push_screen(LoginScreen())
            case "exit":
                await app.action_quit()
            case "view":
                if args[0] == "preferences":
                    app.push_screen(ViewPreferences())
                else:
                    self._log("Second word in input is invalid.")
            case "edit":
                if args[0] == "preferences":
                    app.push_screen(EditPreferences())
                else:
                    self._log("Second word in input is invalid.")
            case "quick":
                if args[0] == "start":
                    self._log("Quick Start command entered.")
                else:
                    self._log("Second word in input is invalid.")
            case _:
                self._log("Unrecognized input.")

    def print_help_message(self) -> None:
        self._log("")


class ViewPreferences(BaseCLIScreen):
    """Screen where user views the preferences associated with their account"""
    def on_mount(self) -> None:
        app = self.get_app()
        self._log(f"Viewing preferences of {app.auth.username}")
        self._log("Type 'help' to see commands.")
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        self.clear_input()
        if not raw:
            return
        
        cmd, *args = raw.split()
        self._handle_commands(cmd, args)
    
    def _handle_commands(self, cmd: str, args: list[str]) -> None:
        # return await super()._handle_commands(cmd, args)
        app = self.get_app()

        match cmd.lower():
            case "help":
                self._log("help command entered.")
            case "exit":
                app.pop_screen()
            case "edit":
                if args[0] == "preferences":
                    app.pop_screen()
                    app.push_screen(EditPreferences())
                else:
                    self._log("Second word in input is invalid.")
            case _:
                self._log("Unrecognized input.")


class EditPreferences(BaseCLIScreen):
    """Screen where user edits the preferences associated with their account"""
    def on_mount(self) -> None:
        app = self.get_app()
        self._log(f"Editing preferences of {app.auth.username}")
        self._log("Type 'exit' to return to the home screen or\nedit preferences to jump to the edit preferences screen.")
        self._log("")
        self._log("Preferences determine how the recommender\ndecides what to recommend.")
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        self.clear_input()
        if not raw:
            return
        
        cmd, *args = raw.split()
        self._handle_commands(cmd, args)
    
    def _handle_commands(self, cmd: str, args: list[str]) -> None:
        # return await super()._handle_commands(cmd, args)
        app = self.get_app()

        match cmd.lower():
            case "help":
                self._log("help command entered.")
            case "exit":
                app.pop_screen()
            case "edit":
                if args[0] == "genre":
                    app.push_screen(EditGenres())
                else:
                    self._log("Second word in input is invalid.")


class EditGenres(BaseCLIScreen):
    """Screen where user edits the genres associated with their account"""
    def on_mount(self) -> None:
        app = self.get_app()
        self._log(f"Editing genres of {app.auth.username}")
        self._log("Type 'exit' to return to the edit screen or\nadd/delete (a/d) followed by the name of the genre\nto add or remove a particular genre from your preferences.")
        self._log("")
        self._log("Genre Options: ")
        self._log("")
        self._log("Preferences determine how the recommender\ndecides what to recommend.")
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        self.clear_input()
        if not raw:
            return
        
        cmd, *args = raw.split()
        self._handle_commands(cmd, args)
    
    def _handle_commands(self, cmd: str, args: list[str]) -> None:
        # return await super()._handle_commands(cmd, args)
        app = self.get_app()

        match cmd.lower():
            case "help":
                self._log("help command entered.")
            case "exit":
                app.pop_screen()
            case "edit":
                if args[0] == "genre":
                    app.push_screen(EditGenres())
                else:
                    self._log("Second word in input is invalid.")


class GameRecommenderApp(App):
    """Textual app which takes credentials sequentially"""

    ENABLE_COMMAND_PALETTE = False
    TITLE = "Game Recommender"
    SUB_TITLE = "Get recommendations for games based on your preferences!"

    def __init__(self):
        super().__init__()
        self.auth = AuthState()
        self.preferences = PreferenceState()

    def on_mount(self) -> None:
        """Runs when the app is started."""
        self.push_screen(LoginScreen())


if __name__ == "__main__":
    GameRecommenderApp().run()