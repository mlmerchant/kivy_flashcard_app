import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.metrics import dp
import random
from flash_cards import flash_card_dictionary


class FlashcardApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cards = flash_card_dictionary.copy()
        self.card_keys = list(self.cards.keys())
        random.shuffle(self.card_keys)
        self.showing_question = True

    def build(self):
        self.current_card = 0
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text=self.card_keys[self.current_card], font_size='30sp', size_hint=(1, 1),
                           text_size=(Window.width - dp(20), None), halign='center', valign='middle', markup=True)
        self.layout.add_widget(self.label)
        self.show_button = Button(text='Show Answer', font_size='30sp', size_hint=(1, 0.2))
        self.show_button.bind(on_press=self.show_answer)
        self.layout.add_widget(self.show_button)

        # Create a horizontal layout for the "Wrong" and "Right" buttons
        self.horizontal_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        self.right_button = Button(text='Right', font_size='30sp')
        self.right_button.bind(on_press=self.right_answer)
        self.horizontal_layout.add_widget(self.right_button)

        self.wrong_button = Button(text='Wrong', font_size='30sp')
        self.wrong_button.bind(on_press=self.wrong_answer)
        self.horizontal_layout.add_widget(self.wrong_button)

        # Add the horizontal layout to the main layout
        self.layout.add_widget(self.horizontal_layout)

        # Bind the on_resize event
        Window.bind(on_resize=self.on_window_resize)

        return self.layout

    def on_window_resize(self, window, width, height):
        self.label.text_size = (width - dp(20), None)

    def show_answer(self, instance):
        if self.showing_question:
            self.label.text = list(self.cards.values())[self.current_card]
            self.show_button.text = 'Show Question'
            self.showing_question = False
        else:
            self.label.text = list(self.cards.keys())[self.current_card]
            self.show_button.text = 'Show Answer'
            self.showing_question = True

    def right_answer(self, instance):
        del self.cards[list(self.cards.keys())[self.current_card]]
        if not self.cards:
            self.label.text = 'You have finished all the cards!'
            self.show_button.disabled = True
            self.right_button.disabled = True
            self.wrong_button.disabled = True
            return
        self.current_card = 0
        self.label.text = list(self.cards.keys())[self.current_card]
        self.show_button.text = 'Show Answer'

    def wrong_answer(self, instance):
        self.current_card = (self.current_card + 1) % len(self.cards)
        self.label.text = list(self.cards.keys())[self.current_card]
        self.show_button.text = 'Show Answer'


if __name__ == '__main__':
    FlashcardApp().run()
