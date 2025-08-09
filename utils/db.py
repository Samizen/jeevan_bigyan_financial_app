# db.py

import sqlite3
import os

# Adjust path based on your project structure
DB_PATH = os.path.join("data", "community_finance.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_categories(tx_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM category WHERE type=?", (tx_type,))
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

def get_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM member")
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

# Helper functions to get IDs from names to insert into transactions table
def get_member_id(member_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Member WHERE name=?", (member_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Helper functions to get IDs from category to insert into transactions table
def get_category_id(category_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Category WHERE name=?", (category_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# The main transaction insertion function
# It takes the member and category names, and then gets the IDs
def insert_transaction(amount, category_name, member_name, date, description):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get the foreign key IDs from the names
    member_id = get_member_id(member_name)
    category_id = get_category_id(category_name)
    
    # Basic validation to ensure we found the IDs
    if member_id is None:
        raise ValueError(f"Member '{member_name}' not found.")
    if category_id is None:
        raise ValueError(f"Category '{category_name}' not found.")
    
    # Corrected INSERT statement using the proper column names and IDs
    cursor.execute("""
        INSERT INTO Transactions (member_id, amount, category_id, description, transaction_date)
        VALUES (?, ?, ?, ?, ?)
    """, (member_id, amount, category_id, description, date))
    
    conn.commit()
    conn.close()

def insert_category(name, tx_type):
    conn = get_connection()
    cursor = conn.cursor()
    type_to_insert = tx_type.capitalize()
    if type_to_insert not in ('Income', 'Expense'):
        # This is an extra safeguard, though the database would catch it anyway
        raise ValueError("Invalid category type. Must be 'Income' or 'Expense'.")
    cursor.execute("INSERT INTO category (name, type) VALUES (?, ?)", (name, type_to_insert))
    conn.commit()
    conn.close()


def insert_member(name, contact_no, member_added_date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Member (name, contact_no, member_added_date)
            VALUES (?, ?, ?)
        """, (name, contact_no, member_added_date))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError(f"Error: Member with name '{name}' already exists.")
    finally:
        conn.close()

def update_transaction(transaction_id, amount, category_name, member_name, date, description):
    conn = get_connection()
    cursor = conn.cursor()

    member_id = get_member_id(member_name)
    category_id = get_category_id(category_name)

    if member_id is None:
        raise ValueError(f"Member '{member_name}' not found.")
    if category_id is None:
        raise ValueError(f"Category '{category_name}' not found.")

    cursor.execute("""
        UPDATE Transactions
        SET member_id = ?, amount = ?, category_id = ?, description = ?, transaction_date = ?
        WHERE id = ?
    """, (member_id, amount, category_id, description, date, transaction_id))

    conn.commit()
    conn.close()


def delete_transaction(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()