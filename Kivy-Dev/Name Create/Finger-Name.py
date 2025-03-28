import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import Textinput 
from kivy.uix.relativelayout import RelativeLayout

# Create the widget
class Finger_text(Widget): 
    pass
  
# Create the app
class FingerApp(App): 
  
    # Building text input 
    def build(self): 
        return text() 
  
    # Arranging that what you write will be shown to you 
    # in IDLE 
    def process(self): 
        text = self.root.ids.input.text 
        print(text) 
  
# Run the App 
if __name__ == "__main__": 
    FingerApp().run() 

