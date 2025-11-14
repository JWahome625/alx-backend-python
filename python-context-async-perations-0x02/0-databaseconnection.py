import sqlite3


class DatabaseConnection:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        """Open the database connection when entering the context."""
        self.conn = sqlite3.connect(self.db_path)
        return self.conn  # returned object is assigned to 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close connection and optionally handle exceptions."""
        if self.conn:
            self.conn.close()

        # Returning False means exceptions (if any) will NOT be suppressed.
        return False
        

# -------------------------------------------
# Using the context manager
# -------------------------------------------

with DatabaseConnection("database.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
