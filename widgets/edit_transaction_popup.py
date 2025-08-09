# widgets/edit_transaction_popup.py

from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, StringProperty
from kivy.lang import Builder
import sqlite3
from widgets.nepali_calendar import NepaliCalendarPopup

Builder.load_file('widgets/edit_transaction_popup.kv')

class EditTransactionPopup(Popup):
    tx_id = NumericProperty()
    on_save_callback = ObjectProperty(None)
    
    # Properties to store data for Spinners
    member_names = ListProperty([])
    category_names = ListProperty([])
    selected_member = StringProperty('')
    selected_category = StringProperty('')

    def on_open(self):
        conn = sqlite3.connect('data/community_finance.db')
        cursor = conn.cursor()

        # 1. Fetch all members
        cursor.execute("SELECT id, name FROM Member")
        members_data = cursor.fetchall()
        self.members_map = {name: mid for mid, name in members_data}
        self.member_names = list(self.members_map.keys())
        
        # 2. Fetch the current transaction data, including category type
        query = """
        SELECT
            t.amount,
            t.description,
            t.transaction_date,
            m.name AS member_name,
            c.name AS category_name,
            c.type AS category_type
        FROM Transactions t
        LEFT JOIN Member m ON t.member_id = m.id
        LEFT JOIN Category c ON t.category_id = c.id
        WHERE t.id=?
        """
        cursor.execute(query, (self.tx_id,))
        data = cursor.fetchone()
        
        # 3. Fetch all categories and filter them by the transaction's type
        if data:
            _, _, _, _, _, transaction_type = data
            cursor.execute("SELECT id, name, type FROM Category WHERE type=?", (transaction_type,))
            categories_data = cursor.fetchall()
            self.categories_map = {name: (cid, ctype) for cid, name, ctype in categories_data}
            self.category_names = list(self.categories_map.keys())

        conn.close()

        if data:
            amount, description, date, member_name, category_name, _ = data
            self.ids.amount_input.text = str(amount)
            self.ids.description_input.text = description or ""
            self.ids.date_input.text = date
            self.ids.member_spinner.text = member_name or "Select Member"
            self.ids.category_spinner.text = category_name or "Select Category"

    def open_calendar(self):
        popup = NepaliCalendarPopup(
            on_select_callback=self.on_date_select
        )
        popup.open()

    def on_date_select(self, year, month, day):
        selected_date_ad = f"{year:04d}-{month:02d}-{day:02d}"
        self.ids.date_input.text = selected_date_ad

    def save(self):
        amount_text = self.ids.amount_input.text.strip()
        description = self.ids.description_input.text.strip()
        date = self.ids.date_input.text.strip()
        member_name = self.ids.member_spinner.text
        category_name = self.ids.category_spinner.text

        try:
            amount = float(amount_text)
        except ValueError:
            return

        member_id = self.members_map.get(member_name)
        category_data = self.categories_map.get(category_name)
        
        if not all([amount, date, member_id, category_data]):
            return

        conn = sqlite3.connect('data/community_finance.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE Transactions
            SET amount=?, description=?, transaction_date=?, member_id=?, category_id=?
            WHERE id=?
        """, (amount, description, date, member_id, category_data[0], self.tx_id))
        
        conn.commit()
        conn.close()

        if self.on_save_callback:
            self.on_save_callback()

        self.dismiss()