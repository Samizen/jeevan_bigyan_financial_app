from datetime import date
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.label import Label

from utils import db

# Load the kv file for this widget
Builder.load_file("widgets/members_form.kv")

class MembersFormPopup(Popup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def submit_member(self):
        member_name = self.ids.member_name_input.text.strip()
        contact_no = self.ids.contact_no_input.text.strip()
        
        if not member_name:
            self.show_error("कृपया सदस्यको नाम प्रविष्ट गर्नुहोस्।")
            return
        
        try:
            member_added_date = date.today().isoformat()
            db.insert_member(member_name, contact_no, member_added_date)
            print(f"✅ नयाँ सदस्य सफलतापूर्वक थपियो: {member_name}")
            self.dismiss()
        except ValueError as e:
            self.show_error(str(e))
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