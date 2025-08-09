from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, ObjectProperty

from kivy.lang import Builder
Builder.load_file('widgets/edit_transaction_popup.kv')

class EditTransactionPopup(Popup):
    tx_id = NumericProperty()
    on_save_callback = ObjectProperty(None)

    def on_open(self):
        import sqlite3
        conn = sqlite3.connect('data/community_finance.db')
        cursor = conn.cursor()
        cursor.execute("SELECT amount, description FROM Transactions WHERE id=?", (self.tx_id,))
        data = cursor.fetchone()
        conn.close()
        if data:
            self.ids.amount_input.text = str(data[0])
            self.ids.description_input.text = data[1] or ""

    def save(self):
        amount_text = self.ids.amount_input.text.strip()
        description = self.ids.description_input.text.strip()
        try:
            amount = float(amount_text)
        except ValueError:
            return  # optionally show error popup here

        import sqlite3
        conn = sqlite3.connect('data/community_finance.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE Transactions SET amount=?, description=? WHERE id=?", (amount, description, self.tx_id))
        conn.commit()
        conn.close()

        if self.on_save_callback:
            self.on_save_callback()

        self.dismiss()
