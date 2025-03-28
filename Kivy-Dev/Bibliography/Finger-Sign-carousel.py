import kivy
from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder


class Dictionary(BoxLayout):
    letter = StringProperty("")

class AlphabetCarousel(App):
    def build(self):
        Builder.load_file("Kivy-Dev/Bibliography/dictionary.kv")
        carousel = Carousel(direction = 'right',loop = True)
        #list of the alphabet
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        for letter in letters:
            slide = Dictionary(letter = letter)
            carousel.add_widget(slide)
        return carousel

if __name__ == "__main__":
    AlphabetCarousel().run()
