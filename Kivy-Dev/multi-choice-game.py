import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivymd.app import MDApp

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions = [
            Question(
                "What letter do you make holding your left index finger straight, the other fingers curled into your palm, and making semi circle with your right thumb and index finger?",
                ["A", "B", "D", "L"],
                "D"
            ),
            Question(
                "Which letter do you make by forming a fist, with the index and middle fingers extended and touching each other together on your other palm?",
                ["N", "O", "G", "S"],
                "N"
            ),
            Question(
                "Which letter is signed by making a fist with the index finger extended touching the opposing thumb?",
                ["M", "A", "S", "T"],
                "A"
            ),
            Question(
                "Which letter is made by holding two fingers apart on the palm while curling the other fingers in?",
                ["V", "W", "U", "N"],
                "V"
            ),
            Question(
                "Which letter is made by holding both hands with their plams open and fingers together",
                ["A", "Z", "P", "B"],
                "B"
            ),
            

        ]
        self.current_question_index = 0
        self.display_question()

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

    def check_answer(self, selected_option):
        #Check if user’s choice matches the current question’s answer.
        current = self.questions[self.current_question_index]
        if selected_option == current.answer:
            print("Correct Answer!")
        else:
            print("Incorrect Answer.")
        self.move_to_next_question()

    def move_to_next_question(self):
        #Advance to the next question or end the game if out of questions.
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            print("Quiz Over!")
            self.game_over()

    def game_over(self):
        #Updates the screen to show a 'Quiz Over!' message and disable buttons.
        self.question_text = "Quiz Over!"
        self.option1 = ""
        self.option2 = ""
        self.option3 = ""
        self.option4 = ""

class QuizApp(MDApp):
    def build(self):
        #dont need this, as quizapp kivy auto loads quiz.kv and this was causing two screens to be built 
        # Load the KV layout
        #Builder.load_file("quiz.kv")

        # Create screen manager, add our QuestionScreen
        sm = ScreenManager()
        sm.add_widget(QuestionScreen(name="question_screen"))
        return sm

if __name__ == "__main__":
    QuizApp().run()
