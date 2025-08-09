from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty, ListProperty

class TransactionRow(BoxLayout):
    # Declare properties that will be used by the .kv file
    tx_id = ObjectProperty(None)
    tx_text = StringProperty('')
    color = ListProperty([1, 1, 1, 1])
    edit_callback = ObjectProperty(None)
    delete_callback = ObjectProperty(None)
    dropdown = ObjectProperty(None)

    def __init__(self, tx_id, tx_text, color, edit_callback, delete_callback, **kwargs):
        super().__init__(**kwargs)
        self.tx_id = tx_id
        self.tx_text = tx_text
        self.color = color
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback
        self.create_dropdown()
        # The Label and Button are now created and styled in the .kv file.

    def create_dropdown(self):
        """Creates the dropdown menu with Edit and Delete buttons."""
        self.dropdown = DropDown()

        btn_edit = Button(text='Edit', size_hint_y=None, height=40)
        btn_edit.bind(on_release=lambda btn: self.select_option('edit'))
        self.dropdown.add_widget(btn_edit)

        btn_delete = Button(text='Delete', size_hint_y=None, height=40)
        btn_delete.bind(on_release=lambda btn: self.select_option('delete'))
        self.dropdown.add_widget(btn_delete)

    def open_menu(self):
        # This method is now called from the .kv file
        # The menu_button is referenced by its ID.
        self.dropdown.open(self.ids.menu_button)

    def select_option(self, option):
        """Handles the selection of an option from the dropdown."""
        self.dropdown.dismiss()
        if option == 'edit':
            self.edit_callback(self.tx_id)
        elif option == 'delete':
            self.delete_callback(self.tx_id)