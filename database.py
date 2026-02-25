import sqlite3
from sqlite3 import Error


class Database:
    def __init__(self, db_name="finance.db"):
        self.db_name = db_name
        self._initialize_database()

    # -----------------------------
    # Connection Handling
    # -----------------------------
    def _connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # allows dict-like access
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    # -----------------------------
    # Schema Initialization
    # -----------------------------
    def _initialize_database(self):
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """

        transactions_table = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            category TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
            description TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        );
        """

        index_query = """
        CREATE INDEX IF NOT EXISTS idx_transactions_user_id
        ON transactions(user_id);
        """

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(users_table)
            cursor.execute(transactions_table)
            cursor.execute(index_query)
            conn.commit()

    # -----------------------------
    # Query Execution
    # -----------------------------
    def execute(self, query, params=()):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        except Error as e:
            raise Exception(f"Database execution error: {e}")

    def fetch_one(self, query, params=()):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

    def fetch_all(self, query, params=()):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
