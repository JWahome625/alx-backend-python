import time
import sqlite3
import functools


query_cache = {}


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
# cache_query decorator
# ---------------------------------------
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query string from kwargs or args
        query = kwargs.get("query")
        if query is None and len(args) > 1:
            query = args[1]  # args[0] = conn, args[1] = query

        # Check cache
        if query in query_cache:
            print("Using cached result for:", query)
            return query_cache[query]

        # Execute actual function
        result = func(*args, **kwargs)

        # Save in cache
        query_cache[query] = result
        print("Caching result for:", query)

        return result

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# ---- First call: runs query and caches result ----
users = fetch_users_with_cache(query="SELECT * FROM users")

# ---- Second call: uses cached result ----
users_again = fetch_users_with_cache(query="SELECT * FROM users")
