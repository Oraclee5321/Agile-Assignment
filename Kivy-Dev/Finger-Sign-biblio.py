import kivy
from kivy.uix.carousel import Carousel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.core.window import Window

class AlphabetCarousel(App):
    def build(self):
        carousel = Carousel(direction = 'right',loop = True)
        #list of the alphabet
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        for letter in letters:
            #slide layout
            slide = Boxlayout(orientation = 'vertical',padding = 20, spacing = 20)
            #label layout
            label = Label(text = letter, font_size = '50sp', bold = True, color=(0,0,0,1))
            #add image
            src = "/Finger-Sign-BSL/%d&.jpg"
            image = AsyncImage(source=src, fit_mode="contain")
            #adding to the slide
            slide.add_widget(slide)
            slide.add_widget(label)
            slide.add_widget(image)
        return carousel

if __name__ == "__main__":
    AlphabetCarousel().run()
