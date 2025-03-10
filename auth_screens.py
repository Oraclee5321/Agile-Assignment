from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from api_client import ApiClientInterface, MockApiClient, LoginStatus, RegisterStatus


class RegisterScreen(Screen):
    """
    Register Screen
    """

    # [Todo]:
    #     Documentation
    #     Improve UI
    #     Check for bad input e.g. empty field (should also be checked serverside, just to reduce requests)
    #     Add parameter for what screen this goes to on register

    def __init__(self, api_client: ApiClientInterface, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.username = TextInput(hint_text="Username", multiline=False)
        self.password = TextInput(hint_text="Password", multiline=False)

        self.register_button: Button = Button(text="Register")
        self.register_button.bind(on_press=self.register)

        self.login_screen_button: Button = Button(text="Login")
        self.login_screen_button.bind(
            on_press=lambda instance: setattr(self.manager, "current", "login")
        )

        self.error_label = Label(text="", color=(1, 0, 0, 1))

        layout.add_widget(Label(text="Register", font_size=24))
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.register_button)
        layout.add_widget(self.login_screen_button)
        layout.add_widget(self.error_label)

        self.add_widget(layout)

    def register(self, instance):
        register_status: RegisterStatus = self.api_client.register(
            self.username.text, self.password.text
        )

        if register_status == RegisterStatus.SUCCESS:
            self.username.text = ""
            self.password.text = ""
            # [Todo]: Make the screen this redirects to a constructor argument
            self.manager.current = "stats"
        else:
            # Handle specific failures later
            self.error_label.text = "Register Failed"

    def on_pre_leave(self, *args):
        self.username.text = ""
        self.password.text = ""
        self.error_label = ""


class LoginScreen(Screen):
    """
    Login Screen
    """

    # [Todo]:
    #     Documentation
    #     Improve UI
    #     Check for bad input e.g. empty field (should also be checked serverside, just to reduce requests)
    #     Add parameter for what screen this goes to on login

    def __init__(self, api_client: ApiClientInterface, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.username = TextInput(hint_text="Username", multiline=False)
        self.password = TextInput(hint_text="Password", multiline=False)

        self.login_button: Button = Button(text="Login")
        self.login_button.bind(on_press=self.login)

        self.register_screen_button: Button = Button(text="Register")
        self.register_screen_button.bind(
            on_press=lambda instance: setattr(self.manager, "current", "register")
        )

        self.error_label = Label(
            text="",
            color=(1, 0, 0, 1),
        )

        layout.add_widget(Label(text="Login", font_size=24))
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.login_button)
        layout.add_widget(self.register_screen_button)
        layout.add_widget(self.error_label)

        self.add_widget(layout)

    def login(self, instance):
        # login
        login_status: LoginStatus = self.api_client.login(
            self.username.text, self.password.text
        )

        if login_status == LoginStatus.SUCCESS:
            # [Todo]: Make the screen this redirects to a constructor argument
            self.manager.current = "stats"
        else:
            # Handle specific failures later
            self.error_label.text = "Login Failed"

    def on_pre_leave(self, *args):
        self.username.text = ""
        self.password.text = ""
        self.error_label.text = ""


class _StatsScreen(Screen):
    """
    Exists purely for showcasing the login and register functionality.
    """

    def __init__(self, api_client: ApiClientInterface, **kw):
        super().__init__(**kw)
        self.api_client = api_client

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.username_label = Label(text="", font_size=18)
        self.coins_label = Label(text="", font_size=18)

        self.logout_button = Button(text="Logout")
        self.logout_button.bind(on_press=self.logout)

        layout.add_widget(self.username_label)
        layout.add_widget(self.coins_label)
        layout.add_widget(self.logout_button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        try:
            self.username_label.text = f"User: {self.api_client.get_username()}"
            self.coins_label.text = f"Coins: {self.api_client.get_coins()}"
        except PermissionError:
            self.manager.current = "login"

    def logout(self, instance):
        # logout code
        self.api_client.logout()
        self.manager.current = "login"


class _LoginTestingApp(App):
    """
    Exists purely for the sake of testing
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = MockApiClient()

    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(
            RegisterScreen(name="register", api_client=self.api_client)
        )
        screen_manager.add_widget(LoginScreen(name="login", api_client=self.api_client))
        screen_manager.add_widget(
            _StatsScreen(name="stats", api_client=self.api_client)
        )
        screen_manager.current = "register"
        return screen_manager


# Run the testing login app if file is ran by itself
# instead of imported
if __name__ == "__main__":
    _LoginTestingApp().run()
