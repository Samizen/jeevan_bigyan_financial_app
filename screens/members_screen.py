# screens/members_screen.py (Corrected)

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from widgets.confirm_delete_popup import ConfirmDeletePopup
from widgets.members_form import MembersFormPopup 
from widgets.member_row import MemberRow 
from utils import db 
from kivy.uix.label import Label 
from kivy.properties import ObjectProperty

Builder.load_file('screens/members_screen.kv')

class MembersScreen(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    
    def on_enter(self, *args):
        self.load_members()

    def load_members(self, search_text=""):
        member_list_container = self.ids.member_list
        member_list_container.clear_widgets()

        members = db.get_members_with_details(search_text)

        if not members:
            member_list_container.add_widget(Label(
                text="कुनै सदस्य फेला परेन।", size_hint_y=None, height=40
            ))
            return

        for member in members:
            member_id, name, contact_no, _ = member
            row = MemberRow(
                member_id=member_id,
                member_name=name,
                contact_no=contact_no,
                edit_callback=self.edit_member,
                delete_callback=self.delete_member
            )
            member_list_container.add_widget(row)
            

    def open_add_member_form(self):
        popup = MembersFormPopup(on_submit_callback=self.on_add_member_submitted)
        popup.open()

    def on_add_member_submitted(self):
        print("Members list refreshed.")
        self.load_members()

    def edit_member(self, member_id):
        member_data = db.get_member_by_id(member_id)
        if not member_data:
            return

        popup = MembersFormPopup(
            member_id=member_id,
            on_submit_callback=self.on_edit_member_submitted,
            name=member_data[0],
            contact_no=member_data[1]
        )
        popup.open()

    def on_edit_member_submitted(self):
        print("Members list refreshed after edit.")
        self.load_members()

    def delete_member(self, member_id):
        confirm_popup = ConfirmDeletePopup(
            message="के तपाईं यो सदस्य मेटाउन निश्चित हुनुहुन्छ?",
            on_confirm=lambda: self._perform_delete(member_id)
        )
        confirm_popup.open()

    def _perform_delete(self, member_id):
        db.delete_member(member_id)
        print(f"Member with ID {member_id} deleted.")
        self.load_members()