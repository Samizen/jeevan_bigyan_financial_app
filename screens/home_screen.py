from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from nepali_datetime import date as nep_date
import datetime
import sqlite3
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


from utils.date_utils import get_nepali_month_range_ad # Assuming this function is in a separate file
from widgets.members_form import MembersFormPopup
from widgets.transactions_form import TransactionFormPopup
from widgets.transaction_row import TransactionRow
from utils.db import delete_transaction
from widgets.nepali_calendar import NepaliCalendarPopup
from widgets.edit_transaction_popup import EditTransactionPopup
from kivy.lang import Builder


DB_PATH = 'data/community_finance.db'

Builder.load_file('widgets/transaction_row.kv')

class HomeScreen(Screen):
    current_month_text = StringProperty()
    income_button_text = StringProperty("आम्दानी: रु 0.00")
    expense_button_text = StringProperty("खर्च: रु 0.00")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.known_balances = {}
        self.set_current_nepali_month()


    def load_known_balances(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT month, starting_balance
            FROM MonthlyBalance
        """)
        rows = cursor.fetchall()
        conn.close()

        self.known_balances = {month: balance for month, balance in rows}

    def on_kv_post(self, base_widget):
        self.load_known_balances()
        self.load_transactions()
        self.refresh_balances()

    def set_current_nepali_month(self):
        today = datetime.date.today()
        nepali_today = nep_date.from_datetime_date(today)
        self.nep_year = nepali_today.year
        self.nep_month = nepali_today.month
        self.update_current_month_text()

    def update_current_month_text(self):
        nepali_months = [
            "", "बैशाख", "जेठ", "असार", "श्रावण", "भदौ", "आश्विन",
            "कार्तिक", "मंसिर", "पौष", "माघ", "फाल्गुन", "चैत्र"
        ]
        month_name = nepali_months[self.nep_month]
        self.current_month_text = f"{month_name} {self.nep_year}"


    def on_month_decrement(self):
        self.nep_month -= 1
        if self.nep_month < 1:
            self.nep_month = 12
            self.nep_year -= 1
        self.update_current_month_text()
        self.load_transactions()
        self.refresh_balances()

    def on_month_increment(self):
        self.nep_month += 1
        if self.nep_month > 12:
            self.nep_month = 1
            self.nep_year += 1
        self.update_current_month_text()
        self.load_transactions()
        self.refresh_balances()

    def get_previous_balance(self, current_month_str):
        if not self.known_balances:
            return 0.0

        earliest_known_month = min(self.known_balances.keys())
        if current_month_str <= earliest_known_month:
            balance = self.known_balances.get(earliest_known_month, 0.0)
            return balance

        year, month = map(int, current_month_str.split('-'))
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
        prev_month_str = f"{year:04d}-{month:02d}"

        if prev_month_str in self.known_balances:
            balance = self.known_balances[prev_month_str]
            return balance

        prev_balance = self.get_previous_balance(prev_month_str)
        income, expense = self.calculate_net_income(prev_month_str)
        balance = prev_balance + (income - expense)
        return balance
    
    def on_transaction_submitted(self):
        self.load_transactions()
        self.refresh_balances()

    def open_add_income_form(self):
        popup = TransactionFormPopup(default_type="income", on_submit_callback=self.on_transaction_submitted)
        popup.open()

    def open_add_expense_form(self):
        popup = TransactionFormPopup(default_type="expense", on_submit_callback=self.on_transaction_submitted)
        popup.open()


    def calculate_net_income(self, nep_month_str):
        
        # Expecting 'YYYY-MM' format here
        try:
            nep_year, nep_month = map(int, nep_month_str.split('-'))
        except ValueError:
            print(f"ERROR: Invalid nep_month_str format: {nep_month_str}. Expected 'YYYY-MM'.")
            return 0.0, 0.0

        nepali_months = [
            "", "बैशाख", "जेठ", "असार", "श्रावण", "भदौ", "आश्विन",
            "कार्तिक", "मंसिर", "पौष", "माघ", "फाल्गुन", "चैत्र"
        ]
        month_name = nepali_months[nep_month]
        nep_month_text = f"{month_name} {nep_year}"
        
        start_date, end_date = get_nepali_month_range_ad(nep_month_text)
        

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                SUM(CASE WHEN c.type = 'Income' THEN t.amount ELSE 0 END),
                SUM(CASE WHEN c.type = 'Expense' THEN t.amount ELSE 0 END)
            FROM Transactions t
            JOIN Category c ON t.category_id = c.id
            WHERE date(t.transaction_date) BETWEEN date(?) AND date(?)
        """, (start_date, end_date))
        income, expense = cursor.fetchone()
        conn.close()

        # Added a print statement to show the raw results from the database query
        
        return (income or 0.0), (expense or 0.0)


    def load_transactions(self, filter_type='month'):
        # Store the current filter type so we can use it for refreshing the list
        self.current_filter = filter_type

        transaction_list = self.ids.transaction_list
        transaction_list.clear_widgets()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Start with the base query
        base_query = """
            SELECT t.id, t.amount, t.transaction_date, t.description,
                m.name AS member_name, c.name AS category_name, c.type
            FROM Transactions t
            LEFT JOIN Member m ON t.member_id = m.id
            LEFT JOIN Category c ON t.category_id = c.id
        """

        conditions = []
        params = []
        today = datetime.date.today()

        # Always filter by the current month's date range
        start_date, end_date = get_nepali_month_range_ad(self.current_month_text)
        conditions.append("date(t.transaction_date) BETWEEN date(?) AND date(?)")
        params.extend([start_date, end_date])
        
        # Add additional conditions based on the filter type
        if filter_type == 'today':
            conditions.append("date(t.transaction_date) = date(?)")
            params.append(today.isoformat())
        elif filter_type == 'week':
            start_of_week = today - datetime.timedelta(days=today.weekday())
            end_of_week = start_of_week + datetime.timedelta(days=6)
            conditions.append("date(t.transaction_date) BETWEEN date(?) AND date(?)")
            params.extend([start_of_week.isoformat(), end_of_week.isoformat()])
        elif filter_type == 'income':
            conditions.append("c.type = 'Income'")
        elif filter_type == 'expense':
            conditions.append("c.type = 'Expense'")
        
        # Combine all conditions and build the final query
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        base_query += " ORDER BY t.transaction_date DESC"

        cursor.execute(base_query, tuple(params))
        transactions = cursor.fetchall()
        conn.close()

        if not transactions:
            transaction_list.add_widget(Label(
                text="कुनै कारोबार फेला परेन।", size_hint_y=None, height=40
            ))
            return

        for tx_id, amount, tx_date, description, member_name, category_name, tx_type in transactions:
            color = (0.2, 0.7, 0.2, 1) if tx_type == 'Income' else (0.7, 0.2, 0.2, 1)
            tx_text = f"{member_name} | {category_name} | {description} | रु {amount} | {tx_date}"
            
            print(f"Generated text: {tx_text}")

            row = TransactionRow(
                tx_id,
                tx_text,
                color,
                self.edit_transaction,
                self.delete_transaction
            )
            transaction_list.add_widget(row)


    def refresh_balances(self):
        current_month_key = f"{self.nep_year:04d}-{self.nep_month:02d}"

        # Note: get_previous_balance recursively calls calculate_net_income
        # So we only need to call calculate_net_income once for the current month.
        prev_balance = self.get_previous_balance(current_month_key)
        income, expense = self.calculate_net_income(current_month_key)
        net = income - expense
        total = prev_balance + net
        
        self.ids.net_result.text = f"शुद्ध नतिजा: रु {net:.2f}"
        self.ids.total_amount.text = f"कुल रकम: रु {total:.2f}"
        self.income_button_text = f"आम्दानी: रु {income:.2f}"
        self.expense_button_text = f"खर्च: रु {expense:.2f}"

    def open_calendar(self):
        popup = NepaliCalendarPopup(
            current_year=self.nep_year,
            on_select_callback=self.on_calendar_select
        )
        popup.open()

    def on_calendar_select(self, year, month):
        self.nep_year = year
        self.nep_month = month
        self.update_current_month_text()
        self.load_transactions()
        self.refresh_balances()

    def open_add_member_form(self):
        # VVVV ADD THIS LOGIC VVVV
        popup = MembersFormPopup()
        popup.open()

    def filter_transactions(self, filter_type):
        self.current_filter = filter_type
        self.load_transactions(filter_type)
        print(f"Filter transactions by: {filter_type}")    

    def edit_transaction(self, tx_id):
        # Create and open the new EditTransactionPopup
        popup = EditTransactionPopup(
            tx_id=tx_id,
            on_save_callback=self.on_transaction_submitted
        )
        popup.open()


    def confirm_delete(self, tx_id, on_confirm):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Are you sure you want to delete this transaction?"))
        buttons = BoxLayout(spacing=10, size_hint_y=None, height=40)
        btn_yes = Button(text="Yes")
        btn_no = Button(text="No")
        buttons.add_widget(btn_yes)
        buttons.add_widget(btn_no)
        content.add_widget(buttons)
        popup = Popup(title="Confirm Delete", content=content, size_hint=(0.6, 0.4), auto_dismiss=False)
        btn_yes.bind(on_release=lambda *args: (on_confirm(tx_id), popup.dismiss()))
        btn_no.bind(on_release=popup.dismiss)
        popup.open()


    def delete_transaction(self, tx_id):
        def on_confirm_delete(tx_id_inner):
            delete_transaction(tx_id_inner)
            self.load_transactions(getattr(self, 'current_filter', 'month'))
            self.refresh_balances()
        # Now we can correctly call self.confirm_delete
        self.confirm_delete(tx_id, on_confirm=on_confirm_delete)

    
