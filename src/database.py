"""
All the database work lives here (Lesson 12).

Keeping the database code in its own file makes app.py shorter and easier to
read. app.py just imports these functions and uses them.
"""

import sqlite3

# Our database file. It stores every review we ever analyze.
DB_FILE = "recipe.db"


def init_db():
    """Create the recipe table the first time we run."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recipe (
            meat TEXT,
            title TEXT,
            recipe TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_results(results):
    """Write all analyzed reviews into the database."""
    conn = sqlite3.connect(DB_FILE)
    for r in results:
        conn.execute(
            "INSERT INTO recipe (meat, title, recipe) VALUES (?, ?, ?)",
            (r["meat"], r["title"], r["recipe"]),
        )
    conn.commit()
    conn.close()


def load_history():
    """Read every recipe we have saved so far."""
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute(
        "SELECT meat, title, recipe FROM recipe"
    ).fetchall()
    conn.close()
    return rows