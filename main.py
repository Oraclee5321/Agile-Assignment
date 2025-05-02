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
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup
from functools import partial


class GameManager:
    def __init__(self):
        self.player = Player()
        self.dark_mode = False
        self.sound_muted = False

class Player:
    def __init__(self, name="Explorer"):
        self.name = name
        self.coins = 50  
        self.inventory = []  # List of tuples (name, image_source)

game = GameManager()


class ThemedButton(Button):
    """Custom button with consistent styling"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = get_color_from_hex('#6fe813')
        self.size_hint = (0.6, None)
        self.height = 50
        self.pos_hint = {'center_x': 0.5}
        self.update_colors()
        
    def update_colors(self):
        if game.dark_mode:
            self.background_color = get_color_from_hex('#3a7309')
            self.color = get_color_from_hex('#ffffff')
        else:
            self.background_color = get_color_from_hex('#6fe813')
            self.color = get_color_from_hex('#000000')


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()
        
        # Will be set in on_pre_enter
        self.background = None
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=20, 
                           size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        # Logo image
        self.logo = Image(source='logo.png.webp', size_hint=(1, 0.3))
        content.add_widget(self.logo)
        
        # Title as backup in case logo fails to load
        self.title_label = Label(text='Wandering Land', font_size='40sp', size_hint=(1, 0.2))
        content.add_widget(self.title_label)
        
        start_button = ThemedButton(text='Start Adventure')
        start_button.bind(on_press=self.start_game)
        content.add_widget(start_button)
        
        self.coin_display = Label(text=f"Coins: {game.player.coins}", size_hint=(1, 0.1))
        content.add_widget(self.coin_display)
        
        # Add some spacing
        content.add_widget(Label(size_hint=(1, 0.1)))
        
        self.layout.add_widget(content)
        self.add_widget(self.layout)
    
    def on_pre_enter(self, *args):
        # Update the UI when entering the screen
        self.update_ui()
        
    def update_ui(self):
        # Remove old background if exists
        if self.background:
            self.layout.remove_widget(self.background)
        
        # Add new background based on dark mode setting
        bg_source = 'background_dark.png' if game.dark_mode else 'background_adventure.png.jpg'
        self.background = Image(source=bg_source, allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background, index=len(self.layout.children))
        
        # Update text colors based on dark mode
        if game.dark_mode:
            self.title_label.color = get_color_from_hex('#ffffff')
            self.coin_display.color = get_color_from_hex('#ffffff')
        else:
            self.title_label.color = get_color_from_hex('#000000')
            self.coin_display.color = get_color_from_hex('#000000')
            
        # Update coin display
        self.coin_display.text = f"Coins: {game.player.coins}"
        
        # Update buttons
        for child in self.walk():
            if isinstance(child, ThemedButton):
                child.update_colors()

    def start_game(self, instance):
        self.manager.current = 'adventure'


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()
        
        # Will be set in on_pre_enter
        self.background = None
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=20, 
                           size_hint=(0.7, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.title_label = Label(text="Log In", font_size='24sp')
        content.add_widget(self.title_label)

        self.username = TextInput(hint_text="Username", size_hint=(1, None), height=40, multiline=False)
        self.password = TextInput(hint_text="Password", password=True, size_hint=(1, None), height=40, multiline=False)
        content.add_widget(self.username)
        content.add_widget(self.password)

        login_button = ThemedButton(text="Log In")
        login_button.bind(on_press=self.login)
        content.add_widget(login_button)

        back_button = ThemedButton(text="Back")
        back_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'adventure'))
        content.add_widget(back_button)

        self.layout.add_widget(content)
        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        self.update_ui()
        
    def update_ui(self):
        # Remove old background if exists
        if self.background:
            self.layout.remove_widget(self.background)
        
        # Add new background based on dark mode setting
        bg_source = 'background_dark.png' if game.dark_mode else 'background_adventure.png.jpg'
        self.background = Image(source=bg_source, allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background, index=len(self.layout.children))
        
        # Update text colors based on dark mode
        if game.dark_mode:
            self.title_label.color = get_color_from_hex('#ffffff')
        else:
            self.title_label.color = get_color_from_hex('#000000')
            
        # Update buttons
        for child in self.walk():
            if isinstance(child, ThemedButton):
                child.update_colors()

    def login(self, instance):
        if self.username.text and self.password.text:
            # For demo purposes, any non-empty username/password will work
            game.player.name = self.username.text
            self.show_notification(f"Welcome, {game.player.name}!")
            self.manager.current = 'adventure'
        else:
            self.show_notification("Please enter both username and password")
    
    def show_notification(self, message):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        
        btn = Button(text='OK', size_hint=(1, None), height=40)
        content.add_widget(btn)
        
        popup = Popup(title='', content=content, size_hint=(0.7, 0.3))
        btn.bind(on_press=popup.dismiss)
        popup.open()


class AdventureScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()
        
        # Will be set in on_pre_enter
        self.background = None
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=20,
                           size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.title_label = Label(text="Welcome to the Adventure!", font_size='24sp')
        content.add_widget(self.title_label)
        
        self.player_info = Label(text=f"Player: {game.player.name} | Coins: {game.player.coins}")
        content.add_widget(self.player_info)

        button_data = [
            ("Log in", self.log_in),
            ("Begin Adventure", self.begin_adventure),
            ("Options", self.open_options),
            ("Shop", self.open_shop),
            ("Virtual Room", self.open_virtual_room),
            ("Back to Home", self.go_back)
        ]

        for text, callback in button_data:
            btn = ThemedButton(text=text)
            btn.bind(on_press=callback)
            content.add_widget(btn)

        self.layout.add_widget(content)
        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        self.update_ui()

    def update_ui(self):
        # Remove old background if exists
        if self.background:
            self.layout.remove_widget(self.background)
        
        # Add new background based on dark mode setting
        bg_source = 'background_dark.png' if game.dark_mode else 'background_adventure.png.jpg'
        self.background = Image(source=bg_source, allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background, index=len(self.layout.children))
        
        # Update text colors based on dark mode
        if game.dark_mode:
            self.title_label.color = get_color_from_hex('#ffffff')
            self.player_info.color = get_color_from_hex('#ffffff')
        else:
            self.title_label.color = get_color_from_hex('#000000')
            self.player_info.color = get_color_from_hex('#000000')
            
        # Update player info
        self.player_info.text = f"Player: {game.player.name} | Coins: {game.player.coins}"
        
        # Update buttons
        for child in self.walk():
            if isinstance(child, ThemedButton):
                child.update_colors()

    def log_in(self, instance):
        self.manager.current = 'login'

    def begin_adventure(self, instance):
        self.show_notification("Adventure starting! Feature coming soon...")

    def open_options(self, instance):
        self.manager.current = 'options'

    def open_shop(self, instance):
        self.manager.current = 'shop'

    def open_virtual_room(self, instance):
        self.manager.current = 'virtual_room'

    def go_back(self, instance):
        self.manager.current = 'main'
        
    def show_notification(self, message):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        
        btn = Button(text='OK', size_hint=(1, None), height=40)
        content.add_widget(btn)
        
        popup = Popup(title='', content=content, size_hint=(0.7, 0.3))
        btn.bind(on_press=popup.dismiss)
        popup.open()


class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()
        
        # Will be set in on_pre_enter
        self.background = None
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=20,
                           size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.title_label = Label(text="Options Menu", font_size='24sp')
        content.add_widget(self.title_label)

        resume_button = ThemedButton(text="Resume")
        resume_button.bind(on_press=self.go_back)
        content.add_widget(resume_button)

        self.sound_button = ThemedButton(text="Mute Sound" if not game.sound_muted else "Unmute Sound")
        self.sound_button.bind(on_press=self.toggle_sound)
        content.add_widget(self.sound_button)

        self.dark_mode_button = ThemedButton(text="Enable Dark Mode" if not game.dark_mode else "Disable Dark Mode")
        self.dark_mode_button.bind(on_press=self.toggle_dark_mode)
        content.add_widget(self.dark_mode_button)

        back_button = ThemedButton(text="Back")
        back_button.bind(on_press=self.go_back)
        content.add_widget(back_button)

        main_menu = ThemedButton(text="Main Menu")
        main_menu.bind(on_press=self.go_to_main)
        content.add_widget(main_menu)

        quit_game = ThemedButton(text="Quit Game")
        quit_game.bind(on_press=self.confirm_quit)
        content.add_widget(quit_game)

        self.layout.add_widget(content)
        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        self.update_ui()

    def update_ui(self):
        # Remove old background if exists
        if self.background:
            self.layout.remove_widget(self.background)
        
        # Add new background based on dark mode setting
        bg_source = 'background_dark.png' if game.dark_mode else 'background_adventure.png.jpg'
        self.background = Image(source=bg_source, allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background, index=len(self.layout.children))
        
        # Update text colors based on dark mode
        if game.dark_mode:
            self.title_label.color = get_color_from_hex('#ffffff')
        else:
            self.title_label.color = get_color_from_hex('#000000')
            
        # Update button texts
        self.sound_button.text = "Unmute Sound" if game.sound_muted else "Mute Sound"
        self.dark_mode_button.text = "Disable Dark Mode" if game.dark_mode else "Enable Dark Mode"
        
        # Update buttons
        for child in self.walk():
            if isinstance(child, ThemedButton):
                child.update_colors()

    def toggle_sound(self, instance):
        game.sound_muted = not game.sound_muted
        self.sound_button.text = "Unmute Sound" if game.sound_muted else "Mute Sound"

    def toggle_dark_mode(self, instance):
        game.dark_mode = not game.dark_mode
        self.dark_mode_button.text = "Disable Dark Mode" if game.dark_mode else "Enable Dark Mode"
        self.update_ui()
        
        # Notify all screens to update their UI
        for screen_name in self.manager.screen_names:
            screen = self.manager.get_screen(screen_name)
            if hasattr(screen, 'update_ui'):
                screen.update_ui()

    def go_back(self, instance):
        self.manager.current = 'adventure'
        
    def go_to_main(self, instance):
        self.manager.current = 'main'
        
    def confirm_quit(self, instance):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Are you sure you want to quit?"))
        
        buttons = BoxLayout(size_hint=(1, None), height=40)
        
        yes_btn = Button(text='Yes')
        yes_btn.bind(on_press=self.quit_game)
        buttons.add_widget(yes_btn)
        
        no_btn = Button(text='No')
        content.add_widget(buttons)
        buttons.add_widget(no_btn)
        
        popup = Popup(title='Confirm', content=content, size_hint=(0.7, 0.3))
        no_btn.bind(on_press=popup.dismiss)
        yes_btn.bind(on_press=popup.dismiss)
        popup.open()
        
    def quit_game(self, instance):
        App.get_running_app().stop()


class ShopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()
        
        # Will be set in on_pre_enter
        self.background = None
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=20,
                           size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.title_label = Label(text="Welcome to the Shop!", font_size='24sp')
        content.add_widget(self.title_label)
        
        self.coin_display = Label(text=f"Your Coins: {game.player.coins}")
        content.add_widget(self.coin_display)

        self.shop_items = [
            ("Chair", "chair.png", 10),
            ("Table", "table.png", 15),
            ("Lamp", "lamp.png", 5),
            ("Bookshelf", "bookshelf.png", 20),
            ("Plant", "plant.png", 8)
        ]

        shop_grid = GridLayout(cols=1, spacing=10, size_hint=(1, None))
        shop_grid.bind(minimum_height=shop_grid.setter('height'))
        
        for name, img, price in self.shop_items:
            item_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=60)
            
            item_label = Label(text=f"{name}", size_hint=(0.4, 1))
            item_layout.add_widget(item_label)
            
            price_label = Label(text=f"{price} Coins", size_hint=(0.3, 1))
            item_layout.add_widget(price_label)
            
            buy_btn = Button(text="Buy", size_hint=(0.3, 0.8), 
                             background_normal='', background_color=get_color_from_hex('#6fe813'))
            buy_btn.bind(on_press=lambda instance, n=name, i=img, p=price: self.buy_item(n, i, p))
            item_layout.add_widget(buy_btn)
            
            shop_grid.add_widget(item_layout)
        
        shop_scroll = BoxLayout(orientation='vertical', size_hint=(1, 0.5))
        shop_scroll.add_widget(shop_grid)
        content.add_widget(shop_scroll)

        back_button = ThemedButton(text="Back")
        back_button.bind(on_press=self.go_back)
        content.add_widget(back_button)

        self.layout.add_widget(content)
        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        self.update_ui()

    def update_ui(self):
        # Remove old background if exists
        if self.background:
            self.layout.remove_widget(self.background)
        
        # Add new background based on dark mode setting
        bg_source = 'background_dark.png' if game.dark_mode else 'background_adventure.png.jpg'
        self.background = Image(source=bg_source, allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background, index=len(self.layout.children))
        
        # Update text colors based on dark mode
        if game.dark_mode:
            self.title_label.color = get_color_from_hex('#ffffff')
            self.coin_display.color = get_color_from_hex('#ffffff')
            
            # Update all labels
            for child in self.walk():
                if isinstance(child, Label):
                    child.color = get_color_from_hex('#ffffff')
        else:
            self.title_label.color = get_color_from_hex('#000000')
            self.coin_display.color = get_color_from_hex('#000000')
            
            # Update all labels
            for child in self.walk():
                if isinstance(child, Label):
                    child.color = get_color_from_hex('#000000')
        
        # Update coin display
        self.coin_display.text = f"Your Coins: {game.player.coins}"
        
        # Update buttons
        for child in self.walk():
            if isinstance(child, ThemedButton):
                child.update_colors()
            elif isinstance(child, Button) and not isinstance(child, ThemedButton):
                if game.dark_mode:
                    child.background_color = get_color_from_hex('#3a7309')
                    child.color = get_color_from_hex('#ffffff')
                else:
                    child.background_color = get_color_from_hex('#6fe813')
                    child.color = get_color_from_hex('#000000')

    def buy_item(self, name, image_source, price):
        if game.player.coins >= price:
            game.player.coins -= price
            game.player.inventory.append((name, image_source))
            self.coin_display.text = f"Your Coins: {game.player.coins}"
            self.show_notification(f"Bought {name}!")
            
            # Update the virtual room's inventory
            virtual_room = self.manager.get_screen('virtual_room')
            if hasattr(virtual_room, 'add_item_to_inventory'):
                virtual_room.add_item_to_inventory(name, image_source)
        else:
            self.show_notification("Not enough coins!")

    def go_back(self, instance):
        self.manager.current = 'adventure'
        
    def show_notification(self, message):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        
        btn = Button(text='OK', size_hint=(1, None), height=40)
        content.add_widget(btn)
        
        popup = Popup(title='', content=content, size_hint=(0.7, 0.3))
        btn.bind(on_press=popup.dismiss)
        popup.open()


class DraggableItem(Scatter):
    def __init__(self, item_name, image_source, room_area, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (120, 120)  # Larger size for better visibility
        self.item_name = item_name
        self.image_source = image_source
        self.room_area = room_area
        
        # Make the item draggable
        self.do_rotation = True  # Allow rotation for more flexibility
        self.do_scale = True     # Allow scaling for resizing
        self.auto_bring_to_front = True
        
        # Create a container for the item (helps with scaling and rotating)
        container = RelativeLayout(size_hint=(1, 1))
        
        # Add the image
        self.item_image = Image(source=image_source, size_hint=(0.9, 0.9), 
                              pos_hint={'center_x': 0.5, 'center_y': 0.5})
        container.add_widget(self.item_image)
        
        # Add item name label for identification
        name_label = Label(text=item_name, font_size='12sp', size_hint=(1, 0.2),
                         pos_hint={'center_x': 0.5, 'y': 0})
        container.add_widget(name_label)
        
        # Add a remove button
        remove_btn = Button(text='X', size_hint=(None, None), size=(25, 25),
                         pos_hint={'right': 1, 'top': 1}, 
                         background_color=(1, 0, 0, 1),
                         font_size='14sp')
        remove_btn.bind(on_press=self.remove_item)
        container.add_widget(remove_btn)
        
        self.add_widget(container)
    
    def remove_item(self, instance):
        # Add the item back to inventory
        virtual_room = self.room_area.parent.parent
        virtual_room.add_item_to_inventory(self.item_name, self.image_source)
        
        # Remove from room
        self.room_area.remove_widget(self)


class VirtualRoomScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = RelativeLayout()
        
        # Will be set in on_pre_enter
        self.background = None
        
        self.room_title = Label(text="Your Virtual Room", font_size='24sp', 
                               size_hint=(1, 0.1), pos_hint={'top': 1})
        self.layout.add_widget(self.room_title)

        # Inventory section
        self.inventory_label = Label(text="Inventory - Click to Place", 
                                    size_hint=(1, 0.05), pos_hint={'top': 0.9})
        self.layout.add_widget(self.inventory_label)

        self.inventory_grid = GridLayout(cols=5, spacing=10, size_hint=(0.9, 0.2), 
                                        pos_hint={'center_x': 0.5, 'top': 0.85})
        self.layout.add_widget(self.inventory_grid)

        # Room area for placing items - now full screen behind everything
        self.room_area = RelativeLayout(size_hint=(1, 0.65), 
                                       pos_hint={'center_x': 0.5, 'y': 0})
        self.layout.add_widget(self.room_area)
        
        # No border needed now since items can be placed anywhere

        back_button = ThemedButton(text="Back to Menu", size_hint=(0.3, 0.1), 
                                 pos_hint={'center_x': 0.5, 'y': 0.02})
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)
        
        # List to track inventory buttons
        self.inventory_buttons = []

    def on_pre_enter(self, *args):
        self.update_ui()
        self.refresh_inventory()

    def update_ui(self):
        # Remove old background if exists
        if self.background:
            self.layout.remove_widget(self.background)
        
        # Add new background based on dark mode setting
        bg_source = 'background_dark.png' if game.dark_mode else 'virtual_room.png'
        self.background = Image(source=bg_source, allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background, index=len(self.layout.children))
        
        # Update text colors based on dark mode
        if game.dark_mode:
            self.room_title.color = get_color_from_hex('#ffffff')
            self.inventory_label.color = get_color_from_hex('#ffffff')
        else:
            self.room_title.color = get_color_from_hex('#000000')
            self.inventory_label.color = get_color_from_hex('#000000')
        
        # Update buttons
        for child in self.walk():
            if isinstance(child, ThemedButton):
                child.update_colors()

    def refresh_inventory(self):
        # Clear current inventory grid
        self.inventory_grid.clear_widgets()
        self.inventory_buttons = []
        
        # Populate with player's inventory
        for item_name, image_source in game.player.inventory:
            self.add_item_to_inventory(item_name, image_source)

    def add_item_to_inventory(self, item_name, image_source):
        item_box = BoxLayout(orientation='vertical', size_hint=(0.15, 1))
        
        # Try to load the image, use fallback if it fails
        try:
            item_btn = Button(background_normal='', background_down='')
            item_image = Image(source=image_source)
            item_btn.add_widget(item_image)
        except:
            # Fallback for testing when image files aren't available
            item_btn = Button(text=item_name[:1], background_normal='', background_color=(0.5, 0.5, 0.8, 1))
        
        item_btn.bind(on_press=lambda instance: self.place_item_in_room(item_name, image_source))
        item_box.add_widget(item_btn)
        
        item_label = Label(text=item_name, size_hint=(1, 0.3))
        item_box.add_widget(item_label)
        
        self.inventory_grid.add_widget(item_box)
        self.inventory_buttons.append((item_name, image_source, item_box))

    def place_item_in_room(self, item_name, image_source):
        # Add the item to the room
        draggable_item = DraggableItem(item_name, image_source, self.room_area)
        draggable_item.pos = (
            self.room_area.width / 2 - draggable_item.width / 2, 
            self.room_area.height / 2 - draggable_item.height / 2
        )
        self.room_area.add_widget(draggable_item)
        
        # Remove the item from inventory
        self.remove_item_from_inventory(item_name, image_source)

    def remove_item_from_inventory(self, item_name, image_source):
        # Find and remove the item button from inventory
        for name, img, item_box in self.inventory_buttons[:]:
            if name == item_name and img == image_source:
                self.inventory_grid.remove_widget(item_box)
                self.inventory_buttons.remove((name, img, item_box))
                
                # Also remove from player inventory
                for i, (inv_name, inv_img) in enumerate(game.player.inventory[:]):
                    if inv_name == item_name and inv_img == image_source:
                        game.player.inventory.pop(i)
                        break
                        
    def go_back(self, instance):
        self.manager.current = 'adventure'


class WanderingLandApp(App):
    def build(self):
        # Set window title
        self.title = 'Wandering Land Adventure'
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add all screens
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(AdventureScreen(name='adventure'))
        sm.add_widget(OptionsScreen(name='options'))
        sm.add_widget(ShopScreen(name='shop'))
        sm.add_widget(VirtualRoomScreen(name='virtual_room'))
        
        # Schedule a callback to handle missing image files
        Clock.schedule_once(self.handle_missing_images, 0.1)
        
        return sm
    
    def handle_missing_images(self, dt):
        """Creates fallback images if the actual image files are missing"""
        from kivy.core.image import Image as CoreImage
        from kivy.graphics.texture import Texture
        from kivy.graphics import Color, Rectangle
        import io
        
        # Create fallback images for testing if real images aren't available
        try:
            # Try to load the background image
            CoreImage('background_adventure.png.jpg')
        except:
            # Create a simple gradient background
            from PIL import Image, ImageDraw
            
            # Create a fallback background
            img = Image.new('RGB', (800, 600), color='darkblue')
            draw = ImageDraw.Draw(img)
            
            # Simple gradient background
            for y in range(600):
                color = (0, 0, 50 + int(y * 0.3))
                draw.line([(0, y), (800, y)], fill=color)
            
            # Save the image
            img.save('background_adventure.png.jpg')
            
            # Create a dark mode version
            img_dark = Image.new('RGB', (800, 600), color='black')
            draw = ImageDraw.Draw(img_dark)
            for y in range(600):
                color = (0, int(y * 0.1), int(y * 0.1))
                draw.line([(0, y), (800, y)], fill=color)
            img_dark.save('background_dark.png')
            
            # Create virtual room background
            img_room = Image.new('RGB', (800, 600), color='beige')
            draw = ImageDraw.Draw(img_room)
            
            # Floor
            draw.rectangle([(0, 300), (800, 600)], fill=(200, 180, 140))
            # Wall
            draw.rectangle([(0, 0), (800, 300)], fill=(230, 220, 200))
            # Window
            draw.rectangle([(500, 50), (700, 200)], fill=(100, 150, 255))
            img_room.save('virtual_room.png')
            
            # Create some item images
            items = {
                'chair.png': (100, 100, 'brown'),
                'table.png': (100, 100, 'brown'),
                'lamp.png': (100, 100, 'yellow'),
                'bookshelf.png': (100, 100, 'brown'),
                'plant.png': (100, 100, 'green')
            }
            
            for name, (width, height, color) in items.items():
                img_item = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
                draw = ImageDraw.Draw(img_item)
                
                if color == 'brown':
                    rgb = (139, 69, 19)
                elif color == 'yellow':
                    rgb = (255, 255, 0)
                elif color == 'green':
                    rgb = (0, 128, 0)
                
                if 'chair' in name:
                    # Simple chair shape
                    draw.rectangle([(20, 60), (80, 80)], fill=rgb)  # seat
                    draw.rectangle([(20, 10), (30, 60)], fill=rgb)  # backrest
                    draw.rectangle([(70, 10), (80, 60)], fill=rgb)  # backrest
                    draw.rectangle([(20, 80), (30, 100)], fill=rgb)  # leg
                    draw.rectangle([(70, 80), (80, 100)], fill=rgb)  # leg
                elif 'table' in name:
                    # Simple table shape
                    draw.rectangle([(10, 60), (90, 70)], fill=rgb)  # top
                    draw.rectangle([(20, 70), (30, 100)], fill=rgb)  # leg
                    draw.rectangle([(70, 70), (80, 100)], fill=rgb)  # leg
                elif 'lamp' in name:
                    # Simple lamp shape
                    draw.rectangle([(40, 70), (60, 100)], fill=(139, 69, 19))  # base
                    draw.rectangle([(45, 40), (55, 70)], fill=(139, 69, 19))  # stem
                    draw.ellipse([(30, 10), (70, 40)], fill=(255, 255, 0))  # shade
                elif 'bookshelf' in name:
                    # Simple bookshelf
                    draw.rectangle([(10, 10), (90, 100)], fill=rgb)  # frame
                    draw.rectangle([(15, 15), (85, 35)], fill=(200, 200, 200))  # shelf
                    draw.rectangle([(15, 40), (85, 60)], fill=(200, 200, 200))  # shelf
                    draw.rectangle([(15, 65), (85, 85)], fill=(200, 200, 200))  # shelf
                elif 'plant' in name:
                    # Simple plant
                    draw.rectangle([(40, 70), (60, 100)], fill=(139, 69, 19))  # pot
                    draw.ellipse([(30, 30), (70, 70)], fill=rgb)  # leaves
                    draw.ellipse([(20, 40), (50, 60)], fill=rgb)  # leaves
                    draw.ellipse([(50, 40), (80, 60)], fill=rgb)  # leaves
                
                img_item.save(name)
                
            print("Created fallback images for testing")
            
            # Also create a logo
            img_logo = Image.new('RGBA', (300, 100), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(img_logo)
            draw.rectangle([(0, 0), (300, 100)], fill=(50, 100, 200, 200))
            draw.text((20, 40), "WANDERING LAND", fill=(255, 255, 255))
            img_logo.save('logo.png.webp')

    def on_stop(self):
        """Clean up resources when the app is closed"""
        print("Wandering Land Adventure is closing...")
        # Add any cleanup code here if needed


if __name__ == '__main__':
    WanderingLandApp().run()





