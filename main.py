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
        cursor = conn.execute(
            "INSERT INTO expenses (date, amount, category, subcategory, note) VALUES (?, ?, ?, ?, ?)",
            (date, amount, category, subcategory, note)
        )
        new_id = cursor.lastrowid
    return {"status": "success", "id": new_id}

@mcp.tool
def list_Expenses():
    """List all expenses from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT id, date, amount, category, subcategory, note FROM expenses ORDER BY id ASC")
        cols = [description[0] for description in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]



@mcp.tool
def list_expense_in_range(start_date, end_date):
    """List expenses within a specified date range."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT id, date, amount, category, subcategory, note FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date ASC",
            (start_date, end_date)
        )
        cols = [description[0] for description in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]
    
@mcp.tool
def edit_expense(expense_id, date, amount, category, subcategory='', note=''):
    """Edit an existing expense by its id."""
    if expense_id is None:
        return {"status": "error", "message": "expense_id is required"}

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "UPDATE expenses SET date = ?, amount = ?, category = ?, subcategory = ?, note = ? WHERE id = ?",
            (date, amount, category, subcategory, note, expense_id)
        )

    if cursor.rowcount == 0:
        return {"status": "not_found", "id": expense_id}
    return {"status": "success", "id": expense_id}

if __name__ == "__main__":
    mcp.run()