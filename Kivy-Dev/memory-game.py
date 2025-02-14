from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.modules import inspector

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
import random

class Methods():
    pass

class MemoryCard(MDCard):
    text = StringProperty()

    def button_test(self):
        if self.ids.img.opacity == 1:
            self.ids.img.opacity = 0
        else:
            self.ids.img.opacity = 1
        print("Button Pressed")

class MemoryScreen(MDScreen):
    def add(self, widget):
        self.ids.grid.add_widget(widget)
    pass

class MemoryGameApp(MDApp):

    def build(self):
        self.screens = MDScreenManager()
        self.screens.add_widget(MemoryScreen(name='home'))
        #size of home
        Window.size = (500, 500)
        inspector.create_inspector(Window, self.screens)
        return self.screens

    def on_start(self):
        for x in range(12):
            rgba = []
            for i in range(3):
                rgba.append(random.random())
            rgba.append(1)

            self.screens.get_screen('home').add(MemoryCard(text=str(x), md_bg_color=rgba))



MemoryGameApp().run()
