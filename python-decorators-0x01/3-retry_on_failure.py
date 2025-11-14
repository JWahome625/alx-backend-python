import time
import sqlite3
import functools


# ---------------------------------------
# with_db_connection decorator
# ---------------------------------------
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("database.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


# ---------------------------------------
# retry_on_failure decorator (with params)
# ---------------------------------------
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == retries:
                        print(f"Failed after {retries} attempts.")
                        raise e
                    print(f"Error: {e}. Retrying in {delay} second(s)...")
                    time.sleep(delay)
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# ----- Attempt to fetch users with automatic retry -----
users = fetch_users_with_retry()
print(users)
