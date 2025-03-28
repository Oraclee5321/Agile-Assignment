from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import get_color_from_hex
from kivy.uix.scatter import Scatter
from kivy.uix.gridlayout import GridLayout


class GameManager:
    def __init__(self):
        self.player = Player()

class Player:
    def __init__(self, name="Explorer"):
        self.name = name
        self.coins = 50  
        self.inventory = []

game = GameManager()


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = RelativeLayout()

        self.background = Image(source='background_adventure.png.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)

        content = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.logo = Image(source='logo.png.webp', size_hint=(1, 0.3))
        content.add_widget(self.logo)

        self.start_button = Button(text='Start Adventure', size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5}, background_normal='')
        self.start_button.background_color = get_color_from_hex('#6fe813')
        self.start_button.bind(on_press=self.start_game)
        content.add_widget(self.start_button)

        layout.add_widget(content)
        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = 'adventure'


class AdventureScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = RelativeLayout()

        self.background = Image(source='background_adventure.png.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)

        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        label = Label(text="Welcome to the Adventure!", font_size='24sp')
        content.add_widget(label)

        button_data = [
            ("Log in", self.log_in),
            ("Begin Adventure", self.begin_adventure),
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

    def begin_adventure(self, instance):
        print("Begin Adventure button pressed")

    def open_options(self, instance):
        self.manager.current = 'options'

    def open_shop(self, instance):
        self.manager.current = 'shop'

    def open_virtual_room(self, instance):
        self.manager.current = 'virtual_room'

    def go_back(self, instance):
        self.manager.current = 'main'


class OptionsScreen(Screen):
    def __init__(self, **kwargs):
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
    def __init__(self, **kwargs):
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
    def __init__(self, **kwargs):
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
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AdventureScreen(name='adventure'))
        sm.add_widget(OptionsScreen(name='options'))
        sm.add_widget(ShopScreen(name='shop'))
        sm.add_widget(VirtualRoomScreen(name='virtual_room'))
        return sm

if __name__ == '__main__':
    WanderingLandApp().run()







