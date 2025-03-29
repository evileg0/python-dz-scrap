import sqlite3
from datetime import datetime

conn = sqlite3.connect('moex_db.db')
cursor = conn.cursor()

def cr_db():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ticker TEXT NOT NULL,
        percent REAL,
        price REAL,
        time TEXT NOT NULL
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    cr_db()