import sqlite3
import asyncio


# -------------------------------
# Async DB helper
# -------------------------------
async def run_query(query, params=()):
    """Runs a blocking SQLite query safely in a thread."""
    def blocking_operation():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        return result

    return await asyncio.to_thread(blocking_operation)


# -------------------------------
# Async functions
# -------------------------------
async def async_fetch_users():
    return await run_query("SELECT * FROM users")


async def async_fetch_older_users():
    return await run_query("SELECT * FROM users WHERE age > ?", (40,))


# -------------------------------
# Concurrent runner
# -------------------------------
async def fetch_concurrently():
    print("Running both queries concurrently...\n")

    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All users:")
    print(all_users)

    print("\nUsers older than 40:")
    print(older_users)


# -------------------------------
# Actual run
# -------------------------------
asyncio.run(fetch_concurrently())
