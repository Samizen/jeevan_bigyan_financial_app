from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.lang import Builder

# Load root_widget kv explicitly for bottom navigation bar
Builder.load_file('widgets/root_widget.kv')

# Load all screen kv files
Builder.load_file('screens/home_screen.kv')
Builder.load_file('screens/members_screen.kv')
Builder.load_file('screens/reports_screen.kv')
Builder.load_file('screens/calculator_screen.kv')
Builder.load_file('screens/settings_screen.kv')
Builder.load_file('widgets/transactions_form.kv')

from widgets.root_widget import RootWidget

# Import screens so they're registered
from screens.home_screen import HomeScreen
from screens.members_screen import MembersScreen
from screens.reports_screen import ReportsScreen
from screens.calculator_screen import CalculatorScreen
from screens.settings_screen import SettingsScreen

# Register font for use in the app
from kivy.core.text import LabelBase
LabelBase.register(
    name='Yantramanav',
    fn_regular='fonts/Yantramanav-Regular.ttf'
)

class FinanceApp(App):
    def build(self):
        return Builder.load_file('financeapp.kv')

if __name__ == '__main__':
    FinanceApp().run()
