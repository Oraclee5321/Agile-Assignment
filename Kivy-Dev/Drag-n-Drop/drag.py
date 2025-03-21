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

class DragGameScreen(MDScreen):
    pass

class DragGameApp(MDApp):
    def build(self):
        self.screens = MDScreenManager()
        self.screens.add_widget(DragGameScreen(name='home'))
        # size of home
        Window.size = (500, 500)
        inspector.create_inspector(Window, self.screens)
        return self.screens
