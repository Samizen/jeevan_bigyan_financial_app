from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.button import Button
from nepali_datetime import date as nep_date
from kivy.properties import NumericProperty

Builder.load_file("widgets/nepali_calendar.kv")

class NepaliCalendarPopup(Popup):
    nep_year = NumericProperty(0)
    
    nepali_months = [
        "बैशाख", "जेठ", "असार", "श्रावण", "भदौ", "आश्विन",
        "कार्तिक", "मंसिर", "पौष", "माघ", "फाल्गुन", "चैत्र"
    ]

    def __init__(self, current_year, on_select_callback, **kwargs):
        super().__init__(**kwargs)
        self.nep_year = current_year
        self.on_select_callback = on_select_callback
        self.populate_months()

    def populate_months(self):
        month_grid = self.ids.month_grid
        month_grid.clear_widgets()
        
        for month_index, month_name in enumerate(self.nepali_months, 1):
            btn = Button(
                text=month_name,
                font_size=18,
                size_hint_y=None,
                height=50
            )
            # We use a lambda to pass the month index to the select function
            btn.bind(on_release=lambda btn, idx=month_index: self.on_month_select(self.nep_year, idx))
            month_grid.add_widget(btn)

    def on_year_increment(self):
        self.nep_year += 1
        self.populate_months()

    def on_year_decrement(self):
        self.nep_year -= 1
        self.populate_months()
    
    def on_month_select(self, year, month):
        # Call the callback function provided by the HomeScreen
        self.on_select_callback(year, month)
        self.dismiss()