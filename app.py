from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = "budget.db"

# ----------------------
# Initialize database
# ----------------------
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ----------------------
# Index route
# ----------------------
@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Fetch transactions
    c.execute("SELECT * FROM transactions ORDER BY date DESC")
    transactions = c.fetchall()

    # Calculate totals
    c.execute("SELECT SUM(amount) FROM transactions WHERE category='Income'")
    total_income = c.fetchone()[0] or 0

    c.execute("SELECT SUM(amount) FROM transactions WHERE category!='Income'")
    total_expenses = c.fetchone()[0] or 0

    net_balance = total_income - total_expenses

    # Expenses by category
    c.execute("SELECT category, SUM(amount) FROM transactions WHERE category!='Income' GROUP BY category")
    rows = c.fetchall()
    categories = [r[0] for r in rows]
    category_totals = [r[1] for r in rows]

    conn.close()

    return render_template(
        "index.html",
        transactions=transactions,
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=net_balance,
        categories=categories,
        category_totals=category_totals
    )

# ----------------------
# Add transaction
# ----------------------
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        description = request.form["description"]
        category = request.form["category"]
        amount = float(request.form["amount"])
        date = request.form["date"] or datetime.today().strftime("%Y-%m-%d")

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(
            "INSERT INTO transactions (description, category, amount, date) VALUES (?, ?, ?, ?)",
            (description, category, amount, date)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("edit.html", transaction=None)

# ----------------------
# Edit transaction
# ----------------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_transaction(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    if request.method == "POST":
        description = request.form["description"]
        category = request.form["category"]
        amount = float(request.form["amount"])
        date = request.form["date"]

        c.execute(
            "UPDATE transactions SET description=?, category=?, amount=?, date=? WHERE id=?",
            (description, category, amount, date, id)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    c.execute("SELECT * FROM transactions WHERE id=?", (id,))
    transaction = c.fetchone()
    conn.close()
    return render_template("edit.html", transaction=transaction)

# ----------------------
# Delete transaction
# ----------------------
@app.route("/delete/<int:id>")
def delete_transaction(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

# ----------------------
# Populate sample data
# ----------------------
@app.route("/populate")
def populate_data():
    sample_transactions = [
        ("Supermarket groceries", "Food & Groceries", 75.50, "2025-08-15"),
        ("Coffee shop", "Food & Groceries", 4.50, "2025-08-16"),
        ("Rent payment", "Housing", 950.00, "2025-08-01"),
        ("Electricity bill", "Utilities", 60.00, "2025-08-10"),
        ("Internet subscription", "Utilities", 40.00, "2025-08-05"),
        ("Gasoline", "Transportation", 45.00, "2025-08-12"),
        ("Netflix subscription", "Entertainment", 15.00, "2025-08-03"),
        ("Gym membership", "Entertainment", 30.00, "2025-08-02"),
        ("Doctor visit", "Healthcare", 50.00, "2025-08-07"),
        ("Pet food", "Miscellaneous", 25.00, "2025-08-08"),
        ("Freelance project", "Income", 300.00, "2025-08-09"),
        ("Gift for friend", "Miscellaneous", 20.00, "2025-08-14")
    ]

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM transactions")
    c.executemany(
        "INSERT INTO transactions (description, category, amount, date) VALUES (?, ?, ?, ?)",
        sample_transactions
    )
    conn.commit()
    conn.close()
    return "Sample transactions added! <a href='/'>Go back</a>"

# ----------------------
# Run the app
# ----------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
