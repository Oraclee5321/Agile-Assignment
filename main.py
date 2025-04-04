from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import get_color_from_hex
from kivy.uix.scatter import Scatter
from kivy.uix.gridlayout import GridLayout

from api_client import MockApiClient
from game_manager import GameManager 


class MainScreen(Screen):
    def __init__(self, game_manager:GameManager, **kwargs):
        super().__init__(**kwargs)
        layout = RelativeLayout()
        self.game_manager = game_manager

        self.background = Image(source='background_adventure.png.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)

        content = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.logo = Image(source='logo.png.webp', size_hint=(1, 0.3))
        content.add_widget(self.logo)

        self.start_button = Button(text='Start Adventure', size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5}, background_normal='')
        self.start_button.background_color = get_color_from_hex('#6fe813')
        self.start_button.bind(on_press=self.start_game)
        content.add_widget(self.start_button)

        self.debug_login_button = Button(text='Debug Login', size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5}, background_normal='')
        self.debug_login_button.background_color = get_color_from_hex('#6fe813')
        self.debug_login_button.bind(on_press=self.debug_login)
        content.add_widget(self.debug_login_button)

        layout.add_widget(content)
        self.add_widget(layout)


    def start_game(self, instance):
        self.manager.current = 'login'

    def debug_login(self, instance):
        # temporary debug login to skip register and login screens for testing
        self.game_manager.api_client.register("debug_user", "debug_password")
        self.game_manager.api_client.login("debug_user", "debug_password")
        self.manager.current = "adventure"

class LoginScreen(Screen):
    def __init__(self, game_manager:GameManager, **kwargs):
        super().__init__(**kwargs)
        self.game_manager = game_manager 
        layout = RelativeLayout()

        self.background = Image(source='background_adventure.png.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)

        content = BoxLayout(orientation='vertical', spacing=10, padding=20, size_hint=(0.7, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        label = Label(text="Log In", font_size='24sp')
        content.add_widget(label)

        self.username = TextInput(hint_text="Username", size_hint=(1, 0.2))
        self.password = TextInput(hint_text="Password", password=True, size_hint=(1, 0.2))
        content.add_widget(self.username)
        content.add_widget(self.password)

        login_button = Button(text="Log In", size_hint=(0.6, 0.2))
        login_button.bind(on_press=self.login)
        content.add_widget(login_button)

        register_button = Button(text="Create new account", size_hint=(0.6, 0.2))
        register_button.bind(on_press=self.open_register)
        content.add_widget(register_button)

        back_button = Button(text="Back", size_hint=(0.4, 0.2))
        back_button.bind(on_press=self.go_back)
        content.add_widget(back_button)

        layout.add_widget(content)
        self.add_widget(layout)

    def login(self, instance):
        # this needs to actually display messages depending on what went wrong
        login_status = self.game_manager.api_client.login(
            self.username.text, self.password.text
        )
        if login_status.success:
            self.manager.current = "adventure"
        else:
            print(login_status.message)

    def open_register(self, instance):
        self.manager.current = "register"

    def go_back(self, instance):
        self.manager.current = "main"


class RegisterScreen(Screen):
    def __init__(self, game_manager:GameManager, **kwargs):
        super().__init__(**kwargs)
        self.game_manager = game_manager
        layout = RelativeLayout()

        self.background = Image(source='background_adventure.png.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)

        content = BoxLayout(orientation='vertical', spacing=10, padding=20, size_hint=(0.7, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        label = Label(text="Register", font_size='24sp')
        content.add_widget(label)

        self.username = TextInput(hint_text="Username", size_hint=(1, 0.2))
        self.password = TextInput(hint_text="Password", password=True, size_hint=(1, 0.2))
        content.add_widget(self.username)
        content.add_widget(self.password)

        register_button = Button(text="Register", size_hint=(0.6, 0.2))
        register_button.bind(on_press=self.register)
        content.add_widget(register_button)

        back_button = Button(text="Back", size_hint=(0.4, 0.2))
        back_button.bind(on_press=self.go_back)
        content.add_widget(back_button)

        layout.add_widget(content)
        self.add_widget(layout)

    def register(self, instance):
        # curently just sends back to login on successful register
        # also needs to have status messages for what went wrong and 
        # to tell user they just created an account
        register_status = self.game_manager.api_client.register(
            self.username.text,
            self.password.text
        )
        if register_status.success:
            self.manager.current = "login"
        else:
            print(register_status.message)

    def go_back(self, instance):
        self.manager.current = "login"


class AdventureScreen(Screen):
    def __init__(self, game_manager:GameManager, **kwargs):
        super().__init__(**kwargs)
        layout = RelativeLayout()

        self.background = Image(source='background_adventure.png.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)

        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        label = Label(text="Welcome to the Adventure!", font_size='24sp')
        content.add_widget(label)

        button_data = [
            # ("Log in", self.log_in),
            # ("Begin Adventure", self.begin_adventure),
            ("Memory Game", self.open_memory_game),
            ("Signs", self.open_signs),
            ("Options", self.open_options),
            ("Shop", self.open_shop),
            ("Virtual Room", self.open_virtual_room),
            ("Back to Home", self.go_back)
        ]

        for text, callback in button_data:
            btn = Button(text=text, size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5}, background_normal='')
            btn.background_color = get_color_from_hex('#6fe813')
            btn.bind(on_press=callback)
            content.add_widget(btn)

        layout.add_widget(content)
        self.add_widget(layout)

    def log_in(self, instance):
        print("Log in button pressed")

    def open_signs(self, instance):
        # self.manager.current = "signs"
        pass

    def open_memory_game(self, instance):
        # self.manager.current = "memory_game"
        pass

    # def begin_adventure(self, instance):
    #     print("Begin Adventure button pressed")

    def open_options(self, instance):
        self.manager.current = 'options'

    def open_shop(self, instance):
        self.manager.current = 'shop'

    def open_virtual_room(self, instance):
        self.manager.current = 'virtual_room'

    def go_back(self, instance):
        self.manager.current = 'main'


class OptionsScreen(Screen):
    def __init__(self, game_manager:GameManager, **kwargs):
        super().__init__(**kwargs)
        layout = RelativeLayout()

        self.background = Image(source='background_adventure.png.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)

        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        label = Label(text="Options Menu", font_size='24sp')
        content.add_widget(label)

        resume_button = Button(text="Resume", size_hint=(0.6, 0.1))
        mute_button = Button(text="Mute Sound", size_hint=(0.6, 0.1))
        dark_mode_button = Button(text="Dark Mode", size_hint=(0.6, 0.1))
        back_button = Button(text="Back", size_hint=(0.6, 0.1))
        main_menu = Button(text="Main Menu", size_hint=(0.6, 0.1))
        quit_game = Button(text="Quit Game", size_hint=(0.6, 0.1))

        back_button.bind(on_press=self.go_back)
        content.add_widget(resume_button)
        content.add_widget(mute_button)
        content.add_widget(dark_mode_button)
        content.add_widget(back_button)
        content.add_widget(main_menu)
        content.add_widget(quit_game)

        layout.add_widget(content)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'adventure'


class ShopScreen(Screen):
    def __init__(self, game_manager:GameManager, **kwargs):
        super().__init__(**kwargs)
        layout = RelativeLayout()

        self.background = Image(source='background_adventure.png.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)

        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        label = Label(text="Welcome to the Shop!", font_size='24sp')
        content.add_widget(label)

        self.shop_items = [
            ("Chair", "chair.png", 10),
            ("Table", "table.png", 15),
            ("Lamp", "lamp.png", 5)
        ]

        for name, img, price in self.shop_items:
            btn = Button(text=f"Buy {name} - {price} Coins", size_hint=(0.6, 0.1), background_normal='')
            btn.background_color = get_color_from_hex('#6fe813')
            btn.bind(on_press=lambda instance, n=name, i=img, p=price: self.buy_item(n, i, p))
            content.add_widget(btn)

        back_button = Button(text="Back", size_hint=(0.3, 0.1))
        back_button.bind(on_press=self.go_back)
        content.add_widget(back_button)

        layout.add_widget(content)
        self.add_widget(layout)

    def buy_item(self, name, image_source, price):
        if game.player.coins >= price:
            game.player.coins -= price
            game.player.inventory.append((name, image_source))
            print(f"Bought {name}!")
            self.manager.get_screen('virtual_room').add_item_to_inventory(name, image_source)
        else:
            print("Not enough coins!")

    def go_back(self, instance):
        self.manager.current = 'adventure'


class VirtualRoomScreen(Screen):
    def __init__(self, game_manager:GameManager, **kwargs):
        super().__init__(**kwargs)
        layout = RelativeLayout()

        self.background = Image(source='background_adventure.png.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)

        self.inventory_label = Label(text="Inventory", size_hint=(1, 0.1), pos_hint={'top': 1}, font_size='20sp')
        layout.add_widget(self.inventory_label)

        self.inventory_grid = GridLayout(cols=4, size_hint=(1, 0.2), pos_hint={'y': 0.75})
        layout.add_widget(self.inventory_grid)

        self.room_area = RelativeLayout(size_hint=(1, 0.6), pos_hint={'y': 0.15})
        layout.add_widget(self.room_area)

        back_button = Button(text="Back to Home", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'y': 0.05},
                             background_normal='', background_color=get_color_from_hex('#6fe813'))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def add_item_to_inventory(self, item_name, image_source):
        item_button = Button(background_normal=image_source, size_hint=(0.2, 0.2))
        item_button.bind(on_press=lambda instance: self.place_item_in_room(image_source))
        self.inventory_grid.add_widget(item_button)

    def place_item_in_room(self, image_source):
        draggable_item = Scatter(size_hint=(0.2, 0.2))
        item_image = Image(source=image_source, size_hint=(1, 1))
        draggable_item.add_widget(item_image)
        self.room_area.add_widget(draggable_item)

    def go_back(self, instance):
        self.manager.current = 'main'

class WanderingLandApp(App):
    def build(self):
        gs = GameManager(MockApiClient())
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main', game_manager=gs))
        sm.add_widget(LoginScreen(name='login', game_manager=gs))
        sm.add_widget(RegisterScreen(name='register', game_manager=gs))
        sm.add_widget(AdventureScreen(name='adventure', game_manager=gs))
        sm.add_widget(OptionsScreen(name='options', game_manager=gs))
        sm.add_widget(ShopScreen(name='shop', game_manager=gs))
        sm.add_widget(VirtualRoomScreen(name='virtual_room', game_manager=gs))
        return sm

if __name__ == '__main__':
    WanderingLandApp().run()







