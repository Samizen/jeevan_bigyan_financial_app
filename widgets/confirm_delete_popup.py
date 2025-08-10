# widgets/confirm_delete_popup.py

from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty

Builder.load_file('widgets/confirm_delete_popup.kv')

class ConfirmDeletePopup(Popup):
    message = StringProperty('')
    on_confirm = ObjectProperty(None)
    
    def confirm_delete(self):
        if self.on_confirm:
            self.on_confirm()
        self.dismiss()