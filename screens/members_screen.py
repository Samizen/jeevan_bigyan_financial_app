from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
import utils.db as Database
# Load the KV file for this screen.
Builder.load_file('screens/members_screen.kv')
from widgets.members_form import MembersFormPopup # <-- Use your existing import

class MembersScreen(Screen):
    db = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    
    def on_enter(self, *args):
        # This method is called when the screen becomes active.
        # It's a good place to load the members from the database.
        self.load_members()

    def load_members(self, search_text=""):
        # We will implement this method in a later step.
        # It will query the database and populate the list.
        pass

    def open_add_member_form(self):
        popup = MembersFormPopup(on_submit_callback=self.on_member_submitted)
        popup.open()


    def on_add_member_submitted(self):
        # We will implement this callback to refresh the list after adding a new member.
        pass