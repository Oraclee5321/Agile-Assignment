import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
import random

gl_version = gl_get_version_major()

if platform == 'win':
    if gl_version <= 2:
        import os
        os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
        set ['KIVY_WINDOW'] = 'dummy'



class Methods():
    pass


class Question:
    def __init__(self, question_text, options, answer):
        self.question_text = question_text
        self.options = options
        self.answer = answer


class QuestionScreen(Screen):
    question_text = StringProperty('')
    option1 = StringProperty('')
    option2 = StringProperty('')
    option3 = StringProperty('')
    option4 = StringProperty('')

    def __init__(self):
        super().__init__()
        # Creating a list of Question objects
        self.questions = [
            Question("What letter do you make with one fist and a straight finger pointing up?", ["A", "B", "D", "L"], "D"),
            Question("Which letter do you make by putting two fingers together on your palm?", ["N", "O", "G", "S"], "N"),
            Question("Which letter is signed by making a fist with the thumb on top?", ["M", "A", "S", "T"], "A"),
            Question("Which letter is made by holding two fingers apart on the palm?", ["V", "W", "U", "N"], "V")
        ]
        self.current_question_index = 0
        self.display_question()

    def display_question(self):
        # Simplify displaying current question and options
        current_question = self.questions[self.current_question_index]
        self.question_text = current_question.question_text
        self.option1 = current_question.options[0]
        self.option2 = current_question.options[1]
        self.option3 = current_question.options[2]
        self.option4 = current_question.options[3]

    def check_answer(self, selected_option):
        current_question = self.questions[self.current_question_index]
        if selected_option == current_question.answer:
            print("Correct Answer!")
        else:
            print("Incorrect Answer.")
        self.move_to_next_question()

    def move_to_next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            print("Quiz Over!")
            self.reset_game()

    def reset_game(self):
        self.current_question_index = 0
        self.display_question()


class QuizApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.question_screen = QuestionScreen()
        self.sm.add_widget(self.question_screen)
        return self.sm

    def on_start(self):
        self.question_screen.display_question()


QuizApp().run()
