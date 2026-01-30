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

@mcp.tool
def list_Expenses():
    """List all expenses from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT id, date, amount, category, subcategory, note FROM expenses ORDER BY id ASC")
        cols = [description[0] for description in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]

# @mcp.tool
# def roll_dice(n_dice : int = 1) -> list[int]:
#     """Roll a specified number of six-sided dice and return the results."""
#     return [random.randint(1, 6) for _ in range(n_dice)]

# @mcp.tool
# def add_two_num(a: int, b: int) -> int:
#     """Add two numbers and return the result."""
#     return a + b


if __name__ == "__main__":
    mcp.run()