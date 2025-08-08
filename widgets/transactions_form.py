from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ListProperty
from kivy.lang import Builder
from datetime import datetime
from nepali_datetime import date as nepali_date
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView

from utils import db  # database functions
from utils.date_utils import bs_to_ad_date 

# Builder.load_file("widgets/transactions_form.kv")  # Adjust path if needed

class TransactionFormPopup(Popup):
    default_type = StringProperty("income")  # Default to income
    categories = ListProperty([])
    members = ListProperty([])

    suggestions_view = None
    on_submit_callback = None

    def __init__(self, on_submit_callback=None, **kwargs):
        self.on_submit_callback = on_submit_callback
        super().__init__(**kwargs)
        self.set_type(self.default_type)
        self.populate_members()
        self.set_today_date()

    def set_type(self, tx_type):
        self.default_type = tx_type
        # Let's get the correct capitalized string here
        if tx_type.lower() == "income":
            db_type = "Income"
        elif tx_type.lower() == "expense":
            db_type = "Expense"
        else:
            # Handle invalid type
            db_type = ""

        self.categories = db.get_categories(db_type)
        self.build_category_buttons()

    def build_category_buttons(self):
        container = self.ids.category_radio_group
        container.clear_widgets()

        for i, name in enumerate(self.categories):
            btn = ToggleButton(
                text=name,
                group="category",
                size_hint_y=None,
                height=40,
                state="down" if i == 0 else "normal"  # Select first by default
            )
            container.add_widget(btn)

    def open_add_category_popup(self):
        

        popup = Popup(title="श्रेणी थप्नुहोस्", size_hint=(0.8, 0.4))
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        label = Label(text="नयाँ श्रेणीको नाम:")
        input_field = TextInput(multiline=False)

        def add_category(instance):
            new_category = input_field.text.strip()
            if new_category:
                db.insert_category(new_category, self.default_type)
                self.set_type(self.default_type)  # refresh categories
            popup.dismiss()

        print(db.get_categories("Income"))
        layout.add_widget(label)
        layout.add_widget(input_field)
        layout.add_widget(Button(text="थप्नुहोस्", on_release=add_category))
        layout.add_widget(Button(text="रद्द गर्नुहोस्", on_release=popup.dismiss))

        popup.content = layout
        popup.open()

    suggestions_view = None

    def populate_members(self):
        self.members = db.get_members()

    def update_member_suggestions(self, text):
        # Dismiss existing suggestions if the input is cleared
        if not text:
            self.dismiss_suggestions()
            return

        suggestions = [m for m in self.members if text.lower() in m.lower()]
        
        if suggestions:
            self.show_member_suggestions(suggestions)
        else:
            self.dismiss_suggestions()

    def show_member_suggestions(self, suggestions):
        # Create a ModalView only if it doesn't exist
        if not self.suggestions_view:
            self.suggestions_view = ModalView(
                size_hint=(None, None),
                size=(self.ids.member_input.width, "200dp"),
                background_color=[0.9, 0.9, 0.9, 1]
            )
            
            # Use a ScrollView to handle a long list of suggestions
            scroll_view = ScrollView()
            self.suggestions_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                spacing='5dp'
            )
            self.suggestions_layout.bind(minimum_height=self.suggestions_layout.setter('height'))
            scroll_view.add_widget(self.suggestions_layout)
            self.suggestions_view.add_widget(scroll_view)

        self.suggestions_layout.clear_widgets()
        for member_name in suggestions:
            btn = Button(
                text=member_name,
                size_hint_y=None,
                height="40dp",
                background_normal="",
                background_color=[1, 1, 1, 1],
                color=[0, 0, 0, 1]
            )
            btn.bind(on_release=self.select_member)
            self.suggestions_layout.add_widget(btn)

        # Position the popup below the TextInput
        input_pos = self.ids.member_input.pos
        input_size = self.ids.member_input.size
        popup_pos_x = input_pos[0]
        popup_pos_y = input_pos[1] - self.suggestions_view.height
        
        self.suggestions_view.pos = popup_pos_x, popup_pos_y
        self.suggestions_view.open()

    def dismiss_suggestions(self, *args):
        if self.suggestions_view:
            self.suggestions_view.dismiss()

    def select_member(self, instance):
        self.ids.member_input.text = instance.text
        self.dismiss_suggestions()


    def set_today_date(self):
        today_bs = nepali_date.today().strftime("%Y-%m-%d")
        self.ids.date_input.text = today_bs

    def get_selected_category(self):
        for widget in self.ids.category_radio_group.children:
            if isinstance(widget, ToggleButton) and widget.state == "down":
                return widget.text
        return None

    def submit_transaction(self):
        amount_text = self.ids.amount_input.text.strip()
        member = self.ids.member_input.text.strip()
        date = self.ids.date_input.text.strip()
        category = self.get_selected_category()
        description = self.ids.description_input.text.strip()
        ad_date_to_db = bs_to_ad_date(date)

        if not (amount_text and member and category and date):
            self.show_error("कृपया सबै आवश्यक जानकारीहरू भर्नुहोस्।")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            self.show_error("रकम गलत छ। कृपया सही अंक प्रविष्ट गर्नुहोस्।")
            return

        if not ad_date_to_db:
            self.show_error("मिति ढाँचा गलत छ।")
            return
        try:
            db.insert_transaction(amount, category, member, ad_date_to_db, description)
            print("✅ लेनदेन सफलतापूर्वक थपियो!")
            print(f"Value of on_submit_callback: {self.on_submit_callback}")
            if self.on_submit_callback:
                print("🚀 Callback is being called!")
                self.on_submit_callback()

            self.dismiss()
        except Exception as e:
            self.show_error(f"त्रुटि: {e}")


    def show_error(self, message):
        popup = Popup(
            title="त्रुटि",
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()
