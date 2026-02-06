from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Header, Input, RichLog

# --- Demo auth store (replace later with real storage) ---
VALID_USERS = {"test": "1234"}


def validate_credentials(username: str, password: str) -> bool:
    return username in VALID_USERS and password == VALID_USERS[username]


# --- App state ---
@dataclass
class AuthState:
    username: str = ""
    is_authed: bool = False


@dataclass
class PreferencesState:
    prefs: Dict[str, str] = field(default_factory=lambda: {
        "genre": "strategy",
        "platform": "pc",
        "difficulty": "normal",
    })


# --- Base Screen with shared UI helpers ---
class BaseCLIScreen(Screen):
    """A screen with a RichLog + Input, CLI-style."""

    prompt: str = "> "

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield RichLog(id="log")
            yield Input(placeholder=self.prompt, id="cmd")

    def on_mount(self) -> None:
        self.query_one("#cmd", Input).focus()

    def _log(self, text: str) -> None:
        self.query_one("#log", RichLog).write(text)

    def clear_input(self) -> None:
        self.query_one("#cmd", Input).value = ""

    def get_app(self) -> "GameRecommenderApp":
        return self.app  # type: ignore[return-value]


# --- Home Screen ---
class HomeScreen(BaseCLIScreen):
    prompt = "home> "

    def on_mount(self) -> None:
        super().on_mount()
        app = self.get_app()
        self._log("Welcome to Game Recommender!")
        self._log("Type 'help' to see commands.")
        if app.auth.is_authed:
            self._log(f"Logged in as: {app.auth.username}")
        else:
            self._log("Not logged in.")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        self.clear_input()
        if not raw:
            return

        app = self.get_app()
        cmd, *args = raw.split()

        match cmd.lower():
            case "help":
                self._log("Commands:")
                self._log("  login               -> go to login screen")
                self._log("  prefs view          -> view preferences")
                self._log("  prefs set k v       -> set preference key k to value v")
                self._log("  logout              -> clear login")
                self._log("  exit                -> quit")
            case "login":
                app.push_screen(LoginScreen())
            case "prefs":
                if not args:
                    self._log("Usage: prefs view | prefs set <key> <value>")
                    return
                sub = args[0].lower()
                if sub == "view":
                    app.push_screen(ViewPreferencesScreen())
                elif sub == "set":
                    if len(args) < 3:
                        self._log("Usage: prefs set <key> <value>")
                        return
                    key, value = args[1], " ".join(args[2:])
                    app.preferences.prefs[key] = value
                    self._log(f"Set preference: {key} = {value}")
                else:
                    self._log("Unknown prefs subcommand. Try: prefs view | prefs set <key> <value>")
            case "logout":
                app.auth = AuthState()
                self._log("Logged out.")
            case "exit" | "quit":
                app.exit()
            case _:
                self._log(f"Unknown command: {cmd}. Type 'help'.")


# --- Login Screen (two-step flow like your current implementation) ---
class LoginScreen(BaseCLIScreen):
    prompt = "login> "

    step: reactive[str] = reactive("username")  # username -> password

    def on_mount(self) -> None:
        super().on_mount()
        self._log("Login")
        self._log("Enter username, then password. Type 'back' to return.")
        self._switch_to_username_mode()

    def _switch_to_username_mode(self) -> None:
        self.step = "username"
        inp = self.query_one("#cmd", Input)
        inp.password = False
        inp.placeholder = "Enter Username:"
        inp.value = ""
        inp.focus()

    def _switch_to_password_mode(self) -> None:
        self.step = "password"
        inp = self.query_one("#cmd", Input)
        inp.password = True
        inp.placeholder = "Enter Password:"
        inp.value = ""
        inp.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        app = self.get_app()
        inp = event.input
        raw = inp.value.strip()

        # Allow navigation commands anytime
        if raw.lower() in {"back", "home"}:
            self.app.pop_screen()
            return
        if raw.lower() in {"exit", "quit"}:
            self.app.exit()
            return

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

            # Clear password ASAP
            inp.value = ""

            if ok:
                app.auth.is_authed = True
                self._log(f"Successfully logged in as {app.auth.username}!")
                self._log("Type 'back' to return home.")
                # keep screen, or auto-return:
                self.app.pop_screen()
            else:
                self._log("Authentication failed, try again.")
                app.auth = AuthState()
                self._switch_to_username_mode()


# --- Preferences Screens ---
class ViewPreferencesScreen(BaseCLIScreen):
    prompt = "prefs(view)> "

    def on_mount(self) -> None:
        super().on_mount()
        app = self.get_app()
        self._log("Preferences (view)")
        self._log("Type 'back' to return.")
        for k, v in app.preferences.prefs.items():
            self.log(f"  {k}: {v}")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip().lower()
        self.clear_input()
        if raw in {"back", "home"}:
            self.app.pop_screen()
        elif raw in {"exit", "quit"}:
            self.app.exit()
        elif raw == "help":
            self._log("Commands: back | exit")
        else:
            self._log("Unknown command. Try: back")


class EditPreferencesScreen(BaseCLIScreen):
    prompt = "prefs(edit)> "

    def on_mount(self) -> None:
        super().on_mount()
        self._log("Preferences (edit)")
        self._log("Usage: set <key> <value>")
        self._log("Type 'back' to return.")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        self.clear_input()
        if not raw:
            return

        app = self.get_app()
        cmd, *args = raw.split()

        if cmd.lower() in {"back", "home"}:
            self.app.pop_screen()
            return
        if cmd.lower() in {"exit", "quit"}:
            self.app.exit()
            return

        if cmd.lower() == "set":
            if len(args) < 2:
                self._log("Usage: set <key> <value>")
                return
            key = args[0]
            value = " ".join(args[1:])
            app.preferences.prefs[key] = value
            self._log(f"Updated: {key} = {value}")
        elif cmd.lower() == "help":
            self._log("Commands: set <key> <value> | back | exit")
        else:
            self._log("Unknown command. Try: set <key> <value> or 'help'.")


# --- App ---
class GameRecommenderApp(App):
    CSS = """
    #log { height: 1fr; }
    #cmd { dock: bottom; }
    """

    ENABLE_COMMAND_PALETTE = False
    TITLE = "Game Recommender"
    SUB_TITLE = "CLI-style navigation with views"

    def __init__(self):
        super().__init__()
        self.auth = AuthState()
        self.preferences = PreferencesState()

    def on_mount(self) -> None:
        # Start at Home
        self.push_screen(HomeScreen())


if __name__ == "__main__":
    GameRecommenderApp().run()