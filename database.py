"""Database module for the Library Management System.  Creates the databases"""

import sqlite3


class DatabaseHandler:
    """Manages SQLite database connections and queries for library books."""

    def __init__(self, db_name="library.db"):
        """Initialize database connection and ensure the schema exists."""
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        """Establish and return a database connection."""
        return sqlite3.connect(self.db_name)

    def create_table(self):
        """Create the books table if it does not already exist.
        
        Primary key is ISBN to uniquely identify each row.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    isbn TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    copies_purchased INTEGER NOT NULL,
                    copies_available INTEGER NOT NULL,
                    retail_price REALL
                )
            """)
            conn.commit()

    def fetch_all_books(self):
        """Retrieve all book records from the database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            return cursor.fetchall()

    def add_book(self, title, author, isbn, purchased, available, price):
        """Insert a new book record into the database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO books (title, author, isbn, copies_purchased, copies_available, retail_price)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (title, author, isbn, purchased, available, price),
            )
            conn.commit()

    def update_book(self, title, author, isbn, purchased, available, price):
        """Update an existing book record matched by ISBN."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE books
                SET title = ?, author = ?, copies_purchased = ?, copies_available = ?, retail_price = ?
                WHERE isbn = ?
            """,
                (title, author, purchased, available, price, isbn),
            )
            conn.commit()

    def delete_book(self, isbn):
        """Delete a book record from the database by its ISBN."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
            conn.commit()