from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

# Define your screen classes
class HomeScreen(Screen):
    pass

class MembersScreen(Screen):
    pass

class IncomeScreen(Screen):
    pass

class ExpenseScreen(Screen):
    pass

class ReportsScreen(Screen):
    pass

class CalculatorScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

# Main App class
class JeevanBigyanApp(App):
    def build(self):
        return Builder.load_file("main.kv")

if __name__ == '__main__':
    JeevanBigyanApp().run()