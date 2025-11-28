
#
# These sources are part of the "PyThon Programming Series" by Edgar Milvus, 
# you can find it on Amazon: https://www.amazon.com/dp/B0FTTQNXKG or
# https://tinyurl.com/PythonProgrammingSeries 
# New books info: https://linktr.ee/edgarmilvus 
#
# MIT License
# Copyright (c) 2025 Edgar Milvus
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Source File: project_advanced_application_script.py
# Description: Advanced Application Script
# ==========================================

import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# --- 1. Configuration and Setup ---

# Define the database file path (using a local file)
DATABASE_FILE = "bookstore_inventory.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Create the Engine: The primary interface to the database
# echo=False keeps the output clean, set to True to see generated SQL
Engine = create_engine(DATABASE_URL, echo=False) 

# Define the Base class for declarative class definitions
Base = declarative_base()

# Configure the Session Factory: This object will create transactional scopes
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=Engine
)

# --- 2. ORM Model Definition ---

class Book(Base):
    """
    Defines the 'books' table structure, mapping Python attributes to database columns.
    """
    __tablename__ = 'books'
    
    # Primary Key and Index
    id = Column(Integer, primary_key=True, index=True)
    
    # Core attributes
    title = Column(String(255), unique=True, nullable=False)
    author = Column(String(255), nullable=False)
    price = Column(Float, default=0.0)
    stock = Column(Integer, default=0)

    def __repr__(self):
        """Provides a readable representation of the object."""
        return f"<Book(ID:{self.id}, title='{self.title}', stock={self.stock}, price=${self.price:.2f})>"

# --- 3. Utility and Session Management ---

def init_db():
    """Creates the database tables based on the ORM models defined in Base."""
    # Base.metadata contains the definitions of all classes inheriting from Base
    Base.metadata.create_all(bind=Engine)
    print(f"Database tables initialized in {DATABASE_FILE}.")

def get_session():
    """
    Dependency management pattern: Provides a managed database session.
    This pattern ensures the session is closed regardless of success or failure.
    """
    db = SessionLocal()
    try:
        # Yields the session instance to the caller (like a Flask request handler)
        yield db
    finally:
        # CRITICAL: Ensures the connection resources are released
        db.close()

# --- 4. CRUD Operations ---

def add_book(db_session, title, author, price, stock):
    """Creates a new Book record and persists it."""
    # Instantiate the Python object
    new_book = Book(title=title, author=author, price=price, stock=stock)
    
    # Stage the object for insertion (Pending state)
    db_session.add(new_book)
    
    # Commit the transaction to write changes to the database
    db_session.commit()
    
    # Refresh the object to load any database-generated values (like 'id')
    db_session.refresh(new_book) 
    print(f"[C] Added: {new_book}")
    return new_book

def find_book_by_title(db_session, title):
    """Retrieves a book by its title using the query API."""
    # Query the Book class, filter results, and retrieve the first match
    book = db_session.query(Book).filter(Book.title == title).first()
    return book

def update_stock(db_session, book_title, delta):
    """Updates the stock count for an existing book."""
    book = find_book_by_title(db_session, book_title)
    if book:
        # Modify the Python object (Dirty state)
        book.stock += delta
        # Commit the transaction to persist the change
        db_session.commit()
        print(f"[U] Updated stock for '{book_title}'. New Stock: {book.stock}")
        return True
    print(f"[U] Error: Book '{book_title}' not found.")
    return False

def remove_book(db_session, book_title):
    """Deletes a book record from the database."""
    book = find_book_by_title(db_session, book_title)
    if book:
        # Mark the object for deletion
        db_session.delete(book)
        # Execute the DELETE statement
        db_session.commit()
        print(f"[D] Removed book: '{book_title}'")
        return True
    return False

# --- 5. Execution Workflow Demonstration ---

if __name__ == "__main__":
    # 5.1 Initialize the database structure
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE) # Start clean for demonstration
    init_db()

    # 5.2 Obtain a managed session instance (Mimicking a request lifecycle)
    # We use next() on the generator for simple synchronous execution
    db_gen = get_session()
    db = next(db_gen) 

    print("\n--- Step A: Adding Initial Inventory ---")
    # C: Create two new books
    book_a = add_book(db, "The Theory of Sessions", "Dr. A. Core", 35.00, 15)
    book_b = add_book(db, "Backend Architectures", "B. Framework", 75.50, 8)

    print("\n--- Step B: Reading and Verification ---")
    # R: Read one book back
    found_book = find_book_by_title(db, "The Theory of Sessions")
    print(f"[R] Verified entry: {found_book}")

    print("\n--- Step C: Inventory Update (Restock and Sale) ---")
    # U: Update stock (Restock +5, Sale -3)
    update_stock(db, "The Theory of Sessions", 5)
    update_stock(db, "Backend Architectures", -3) 

    print("\n--- Step D: Deleting Discontinued Item ---")
    # D: Delete the first book
    remove_book(db, "The Theory of Sessions")

    print("\n--- Step E: Final Inventory Check ---")
    # Final Read of all remaining books
    remaining_books = db.query(Book).all()
    print(f"Total remaining items: {len(remaining_books)}")
    for book in remaining_books:
        print(f"-> {book}")

    # 5.3 Close the session (required by the generator pattern)
    try:
        next(db_gen)
    except StopIteration:
        # The generator cleanup code (finally block) has executed
        print("\nSession closed successfully.")
