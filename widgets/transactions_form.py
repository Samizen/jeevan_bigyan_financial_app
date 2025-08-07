from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

import datetime
import db  # Assuming you have db.py with get_categories and get_members

def get_nepali_date_today():
    # Replace with your nepali date logic if available
    return "2082-04-22"  # Example static fallback

class TransactionFormPopup(Popup):
    default_type = StringProperty("income")
    default_date = StringProperty(get_nepali_date_today())
    categories_income = ListProperty()
    categories_expense = ListProperty()
    member_dropdown = ObjectProperty(None)

    def __init__(self, on_submit_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.on_submit_callback = on_submit_callback
        Clock.schedule_once(self.load_initial_data)

    def load_initial_data(self, *args):
        self.categories_income = db.get_categories("income")
        self.categories_expense = db.get_categories("expense")
        self.members = db.get_members()
        self.setup_member_search()
        self.load_categories()

    def set_type(self, tx_type):
        self.default_type = tx_type
        self.load_categories()

    def load_categories(self, *args):
        container = self.ids.category_radio_group
        container.clear_widgets()

        categories = self.categories_income if self.default_type == "income" else self.categories_expense

        for cat in categories:
            btn = ToggleButton(
                text=cat,
                group="category",
                size_hint_y=None,
                height=40,
                allow_no_selection=False
            )
            container.add_widget(btn)

    def get_selected_category(self):
        for widget in self.ids.category_radio_group.children:
            if isinstance(widget, ToggleButton) and widget.state == "down":
                return widget.text
        return None

    def setup_member_search(self):
        dropdown = DropDown()
        self.member_dropdown = dropdown

        self.ids.member_input.bind(text=self.on_member_input)

        for name in self.members:
            btn = Button(text=name, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.select_member(btn.text))
            dropdown.add_widget(btn)

    def on_member_input(self, instance, value):
        self.member_dropdown.clear_widgets()
        for name in self.members:
            if value.lower() in name.lower():
                btn = Button(text=name, size_hint_y=None, height=30)
                btn.bind(on_release=lambda btn: self.select_member(btn.text))
                self.member_dropdown.add_widget(btn)
        self.member_dropdown.open(instance)

    def select_member(self, name):
        self.ids.member_input.text = name
        self.member_dropdown.dismiss()

    def submit_form(self):
        amount = self.ids.amount_input.text.strip()
        date = self.ids.date_input.text.strip()
        description = self.ids.description_input.text.strip()
        category = self.get_selected_category()
        member = self.ids.member_input.text.strip()

        if not amount or not category or not date or not member:
            print("All required fields must be filled.")
            return

        try:
            amount = float(amount)
        except ValueError:
            print("Invalid amount.")
            return

        data = {
            "type": self.default_type,
            "amount": amount,
            "category": category,
            "date": date,
            "description": description,
            "member": member
        }

        if self.on_submit_callback:
            self.on_submit_callback(data)

        self.dismiss()
