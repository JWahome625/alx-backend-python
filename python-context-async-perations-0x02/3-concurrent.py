import asyncio
import aiosqlite


# -------------------------------
# Async functions using aiosqlite
# -------------------------------
async def async_fetch_users():
    async with aiosqlite.connect("database.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        result = await cursor.fetchall()
        await cursor.close()
        return result


async def async_fetch_older_users():
    async with aiosqlite.connect("database.db") as db:
        cursor = await db.execute(
            "SELECT * FROM users WHERE age > ?", (40,)
        )
        result = await cursor.fetchall()
        await cursor.close()
        return result


# -------------------------------
# Run both queries concurrently
# -------------------------------
async def fetch_concurrently():
    print("Fetching users concurrently...\n")

    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All users:")
    print(all_users)

    print("\nUsers older than 40:")
    print(older_users)


# -------------------------------
# Run the async program
# -------------------------------
asyncio.run(fetch_concurrently())
