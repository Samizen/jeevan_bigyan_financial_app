from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class RootWidget(BoxLayout):
    screen_manager = ObjectProperty(None)

    def switch_screen(self, screen_name):
        self.screen_manager.current = screen_name
