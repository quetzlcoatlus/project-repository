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
    step: reactive[str] = reactive("username") # username -> password

    def on_mount(self) -> None:
        super().on_mount()
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
    
    def on_mount(self) -> None:
        super().on_mount()
        app = self.get_app()
        self._log(f"{app.auth.username} welcome to Game Recommender!")
        self._log("Type 'help' to see commands.")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        self.clear_input()
        if not raw:
            return
        
        app = self.get_app()
        cmd, *args = raw.split()

        match cmd.lower():
            case "help":
                self._log("help command entered.")
            case "logout":
                app.auth = AuthState()
                app.pop_screen()
                app.push_screen(LoginScreen())

        





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