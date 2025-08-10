# widgets/member_row.py

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.lang import Builder
# from widgets.member_action_menu import MemberActionMenu

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label

Builder.load_file('widgets/member_row.kv')

class MemberRow(BoxLayout):
    member_id = NumericProperty(0)
    member_name = StringProperty('')
    contact_no = StringProperty('')
    
    edit_callback = ObjectProperty(None)
    delete_callback = ObjectProperty(None)

    
    def __init__(self, member_id, member_name, contact_no, edit_callback=None, delete_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.member_id = member_id
        self.member_name = member_name
        self.contact_no = contact_no
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback


    def open_actions_menu(self):
        if not self.edit_callback or not callable(self.edit_callback):
            print(f"[ERROR] edit_callback not set or not callable for member {self.member_id}")
            return
        if not self.delete_callback or not callable(self.delete_callback):
            print(f"[ERROR] delete_callback not set or not callable for member {self.member_id}")
            return
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        btn_edit = Button(text='Edit')
        btn_delete = Button(text='Delete')
        content.add_widget(btn_edit)
        content.add_widget(btn_delete)

        popup = Popup(title='Actions', content=content, size_hint=(0.4, 0.3))

        btn_edit.bind(on_release=lambda *a: (self.edit_callback(self.member_id), popup.dismiss()))
        btn_delete.bind(on_release=lambda *a: (self.delete_callback(self.member_id), popup.dismiss()))

        popup.open()