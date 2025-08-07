import sqlite3
import random
from datetime import datetime, timedelta

# --- Setup ---
DB_NAME = "community_finance.db"

# --- Create database and connect ---
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# --- Drop tables if re-running the script ---
cursor.executescript("""
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Category;
""")

# --- Create Tables ---
cursor.execute("""
CREATE TABLE Member (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_no TEXT,
    member_added_date DATE
);
""")

cursor.execute("""
CREATE TABLE Category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT CHECK(type IN ('Income', 'Expense')),
    name TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE Transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    amount REAL NOT NULL,
    category_id INTEGER,
    description TEXT,
    transaction_date DATE,
    FOREIGN KEY(member_id) REFERENCES Member(id),
    FOREIGN KEY(category_id) REFERENCES Category(id)
);
""")

# --- Add Dummy Members ---
member_names = [f"Member {i}" for i in range(1, 11)]
for name in member_names:
    contact = f"98{random.randint(10000000, 99999999)}"
    added_date = datetime(2025, 4, 13).date()  # Baisakh 1
    cursor.execute("INSERT INTO Member (name, contact_no, member_added_date) VALUES (?, ?, ?)",
                   (name, contact, added_date))

# --- Add Dummy Categories ---
categories = [
    ('Income', 'Donation'),
    ('Income', 'Membership Fee'),
    ('Income', 'Interest'),
    ('Expense', 'Utilities'),
    ('Expense', 'Events'),
    ('Expense', 'Maintenance')
]
for cat_type, name in categories:
    cursor.execute("INSERT INTO Category (type, name) VALUES (?, ?)", (cat_type, name))

# --- Get IDs for reference ---
cursor.execute("SELECT id FROM Member")
member_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id, type FROM Category")
category_data = cursor.fetchall()
income_categories = [cat[0] for cat in category_data if cat[1] == 'Income']
expense_categories = [cat[0] for cat in category_data if cat[1] == 'Expense']

# --- Generate Transactions from Baisakh 1 (April 13) to Shrawan (~August) ---
start_date = datetime(2025, 4, 13)
end_date = datetime(2025, 8, 5)

transactions = []

for _ in range(100):
    member_id = random.choice(member_ids)
    is_income = random.choice([True, False])
    category_id = random.choice(income_categories if is_income else expense_categories)
    amount = round(random.uniform(100, 2000), 2)
    description = "Monthly transaction" if random.random() < 0.6 else "Special case"
    days_offset = random.randint(0, (end_date - start_date).days)
    transaction_date = (start_date + timedelta(days=days_offset)).date()

    transactions.append((member_id, amount, category_id, description, transaction_date))

cursor.executemany("""
INSERT INTO Transactions (member_id, amount, category_id, description, transaction_date)
VALUES (?, ?, ?, ?, ?)
""", transactions)

# --- Commit and close ---
conn.commit()
conn.close()

print(f"✅ Database '{DB_NAME}' created with sample data.")
