import sqlite3


class ExecuteQuery:
    def __init__(self, query, params=None, db_path="database.db"):
        self.query = query
        self.params = params or ()
        self.db_path = db_path
        self.conn = None
        self.result = None

    def __enter__(self):
        # Open DB connection
        self.conn = sqlite3.connect(self.db_path)

        # Execute the query
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()

        # Return result directly
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Always close the connection
        if self.conn:
            self.conn.close()

        # Do not suppress exceptions
        return False


# ---------------------------------------------------
# Using the context manager
# ---------------------------------------------------

query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params) as results:
    print(results)
