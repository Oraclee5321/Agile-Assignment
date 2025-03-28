import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivymd.app import MDApp
#importing question data from file
import json
from pathlib import Path

class Question:
    def __init__(self, question_text, options, answer):
        self.question_text = question_text
        self.options = options
        self.answer = answer
class MenuScreen(Screen):
    pass

class QuestionScreen(Screen):
    question_text = StringProperty('')
    option1 = StringProperty('')
    option2 = StringProperty('')
    option3 = StringProperty('')
    option4 = StringProperty('')

    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        questions_file = "Multi Game/question-data.json"
        self.questions_list = self.load_questions_from_json(questions_file)
    
        # If the chosen difficulty is 'hard',
        # replace each question's text with "WIP".
        if app.difficulty == "hard":
            for q in self.questions_list:
                q.update(
                    question_text="WIP",
                    options=["WIP"] * 4,
                    answer="WIP")

        self.questions = [Question(**q) for q in self.questions_list]
        self.current_question_index = 0
        self.display_question()

        
    def load_questions_from_json(self, filename):
        # Make sure the file path is correct
        path = Path(filename)
        if not path.is_file():
            print(f"File not found: {filename}")
            return []
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def display_question(self):
        #Set the screen text to match the current question and options.
        if self.current_question_index < len(self.questions):
            current = self.questions[self.current_question_index]
            self.question_text = current.question_text
            self.option1 = current.options[0]
            self.option2 = current.options[1]
            self.option3 = current.options[2]
            self.option4 = current.options[3]
        else:
            # If we somehow exceed the list, show "Quiz Over!"
            self.game_over()

    def move_to_next_question(self):
        #Advance to the next question or end the game if out of questions.
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            print("Quiz Over!")
            self.game_over()

    def check_answer(self, selected_option):
        #Check if user’s choice matches the current question’s answer.
        current = self.questions[self.current_question_index]
        if selected_option == current.answer:
            print("Correct Answer!")
        else:
            print("Incorrect Answer.")
        self.move_to_next_question()

    def game_over(self):
        #Updates the screen to show a 'Quiz Over!' message and disable buttons.
        self.question_text = "Quiz Over!"
        self.option1 = ""
        self.option2 = ""
        self.option3 = ""
        self.option4 = ""

class QuizApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.difficulty = None  # Will store either 'easy' or 'hard'

    def set_difficulty(self, diff):
        self.difficulty = diff

    def build(self):
        #dont need this, as quizapp kivy auto loads quiz.kv and this was causing two screens to be built 
        # Load the KV layout
        #Builder.load_file("quiz.kv")
        # Create screen manager 
        sm = ScreenManager()
        #add MenuScreen
        sm.add_widget(MenuScreen(name="menu_screen"))
        #add QuestionScreen
        sm.add_widget(QuestionScreen(name="question_screen"))
        sm.current = "menu_screen"
        return sm

if __name__ == "__main__":
    QuizApp().run()
