import os
from fastmcp import FastMCP
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'test_expensetracker.db')

mcp = FastMCP(name="expensetracker")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """ CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
            """
        )

init_db()   

@mcp.tool
def add_expenses(date,amount,category,subcategory='',note=''):
    """Add a new expense to the database."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO expenses (date, amount, category, subcategory, note) VALUES (?, ?, ?, ?, ?)",
            (date, amount, category, subcategory, note)
        )
    return {"status": "success", "id": conn.lastrowid} 

if __name__ == "__main__":
    mcp.run()