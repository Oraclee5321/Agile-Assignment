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
from kivy.uix.behaviors import DragBehavior
from kivy.uix.label import Label

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
import random
import os

class DragLabel(DragBehavior, Label):
    text = StringProperty()
    id = StringProperty()



class DragScreen(MDScreen):
    score = NumericProperty(0)

    def generate_drag_boxes(self):
        for x in range(5):
            new_label = DragLabel()
            new_label.text = str(x)
            new_label.size_hint = (0.25, 0.2)
            self.ids.grid.add_widget(new_label)
        for item in self.ids.grid.children:
            item.pos = random.randint(0, 500), random.randint(0, 500)






    def generate_answer_boxes(self):
        pass

    def on_enter(self, *args):
        self.ids.grid.clear_widgets()
        self.generate_drag_boxes()
        self.generate_answer_boxes()


class DragGameApp(MDApp):
    def build(self):
        self.screens = MDScreenManager()
        self.screens.add_widget(DragScreen(name='home'))
        # size of home
        Window.size = (500, 500)
        inspector.create_inspector(Window, self.screens)
        return self.screens

DragGameApp().run()