from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

class HomeScreen(Screen):
    current_month_text = StringProperty("बैशाख २०७९")  # Default Nepali month example

    def on_month_decrement(self):
        print("Previous month button pressed")
        # TODO: Update month and refresh data

    def on_month_increment(self):
        print("Next month button pressed")
        # TODO: Update month and refresh data

    def open_calendar(self):
        print("Open Nepali calendar picker overlay")
        # TODO: Implement calendar popup for month/year choosing

    def open_income_form(self):
        print("Open income form overlay")
        # TODO: Implement income form overlay

    def open_expense_form(self):
        print("Open expense form overlay")
        # TODO: Implement expense form overlay

    def open_add_member_form(self):
        print("Open add member form overlay")
        # TODO: Implement add member form overlay

    def filter_transactions(self, filter_type):
        print(f"Filter transactions by: {filter_type}")
        # TODO: Implement filtering logic
