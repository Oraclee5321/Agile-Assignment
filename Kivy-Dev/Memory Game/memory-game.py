import copy

from kivy.app import App
from kivy.graphics.opengl_utils import gl_get_version_major
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.modules import inspector
from kivy.utils import platform


from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
import random
import os

class Methods():
    pass

class MemoryCard(MDCard):
    text = StringProperty() # Replace with image property
    id = StringProperty() # Card ID
    pressed = BooleanProperty(False) # Game Attribute
    linked_card = None # Game Attribute

    def button_click(self):
        print("Hello")
        if self.ids.img.disabled == True:
            return
        parent = self.parent.parent
        if parent.current_card == None and self.ids.img.disabled != True:
            parent.current_card = self
        if self.ids.img.opacity == 0:
            print("Show")
            self.ids.img.opacity = 1
            self.pressed = True
            if parent.clicked == True:
                self.logic_check(parent)
                parent.clicked = False
            else:
                parent.clicked = True

    def reset(self):
        parent = self.parent.parent
        parent.lives -= 1
        if self.ids.img.disabled != True:
            self.ids.img.opacity = 0
            self.pressed = False
            parent.clicked = False
        if parent.current_card != None and parent.current_card.ids.img.disabled != True:
            parent.current_card.ids.img.opacity = 0
            parent.current_card.pressed = False
            parent.current_card = None


    def logic_check(self,parent):

        if self.linked_card.pressed == True:
            self.ids.img.disabled =  True
            self.linked_card.ids.img.disabled = True
            parent.current_card = None
            parent.score += 1
            print("Match")
        else:
            self.reset()
            print("No Match")
        print("Logic Check")

class MemoryScreen(MDScreen):
    clicked = BooleanProperty(False)
    score = NumericProperty(0)
    lives = NumericProperty(6)
    current_card = None
    def add(self, widget):
        self.ids.grid.add_widget(widget)
    pass

class MemoryGameApp(MDApp):

    def build(self): # Create Screen Manager
        self.screens = MDScreenManager()
        self.screens.add_widget(MemoryScreen(name='home'))
        #size of home
        Window.size = (500, 500)
        inspector.create_inspector(Window, self.screens)
        return self.screens

    def on_start(self):
        self.generate_cards()

    def generate_cards(self): # Generate Cards for memory game
        nums1, nums2 = [x for x in range(6)], [x for x in range(6)]
        random.shuffle(nums1)
        random.seed(len(nums1) * len(nums2) + 1)
        random.shuffle(nums2)
        images = os.listdir('../img/memory-card-img')
        while nums1 != [] and nums2 != []:
            # Implement images and shuffle
            x = nums1.pop()
            y = nums2.pop()
            rgba = [random.random() for _ in range(3)] + [1]
            self.screens.get_screen('home').add(MemoryCard(text=str(x), id=str(x), md_bg_color=rgba))
            self.screens.get_screen('home').add(MemoryCard(text=str(y), id=str(y), md_bg_color=rgba))
        cards = copy.copy(self.screens.get_screen('home').ids.grid.children)
        x = 0
        y = -1
        while cards != []:
            try:
                flag = False
                selected = cards.pop()
                while flag != True:
                    if selected.id == cards[y].id:
                        selected.linked_card = cards[y]
                        cards[y].linked_card = selected
                        cards.pop(y)
                        flag = True
                    elif selected.id == cards[x].id:
                        selected.linked_card = cards[x]
                        cards[x].linked_card = selected
                        cards.pop(x)
                        flag = True
                    else:
                        y -= 1
                        x += 1
                x = 0
                y = -1
            except AttributeError:
                continue





MemoryGameApp().run()
