import sqlite3

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect('budget.db')
c = conn.cursor()

# Create transactions table
c.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    category TEXT,
    amount REAL,
    date TEXT
)
''')

conn.commit()
conn.close()
print("Database and table created!")
