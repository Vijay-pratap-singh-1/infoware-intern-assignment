import sqlite3
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Set correct database path
DB_PATH = resource_path("infoware.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_master (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT,
            sku_id TEXT,
            category TEXT,
            subcategory TEXT,
            product_image TEXT,
            product_name TEXT,
            description TEXT,
            tax REAL,
            price REAL,
            unit TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goods_receiving (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            supplier_name TEXT,
            quantity INTEGER,
            unit TEXT,
            rate_per_unit REAL,
            total REAL,
            tax REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            customer_name TEXT,
            quantity INTEGER,
            unit TEXT,
            rate_per_unit REAL,
            total REAL,
            tax REAL
        )
    ''')

    # Insert default operator logins if not already present
    cursor.execute("SELECT COUNT(*) FROM operators")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany('''
            INSERT INTO operators (username, password) VALUES (?, ?)
        ''', [
            ('operator1', 'pass123'),
            ('operator2', 'admin456')
        ])
        conn.commit()
        print("Inserted default operator logins.")

    conn.commit()
    conn.close()
    print("Database created and initialized successfully.")

def get_connection():
    return sqlite3.connect(DB_PATH)

if __name__ == "__main__":
    init_db()
