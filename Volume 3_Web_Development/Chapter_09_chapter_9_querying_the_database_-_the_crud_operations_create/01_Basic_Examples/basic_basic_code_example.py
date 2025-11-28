
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

# Source File: basic_basic_code_example.py
# Description: Basic Code Example
# ==========================================

from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# 1. SETUP: Define the database connection and model structure
# We use an in-memory SQLite database for simplicity.
# The engine manages the connection to the database.
ENGINE = create_engine("sqlite:///:memory:", echo=False) 

# Base is a factory that will link our Python classes to the tables.
Base = declarative_base()

# Define the Book model (our table structure)
class Book(Base):
    # __tablename__ specifies the name of the table in the database
    __tablename__ = 'books'
    
    # Define columns and their SQL types
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)

    def __repr__(self):
        # A helpful method for printing the object cleanly
        return f"Book(id={self.id}, title='{self.title}', author='{self.author}')"

# Create the tables defined in Base within the database linked to the ENGINE
Base.metadata.create_all(ENGINE)

# 2. SESSION MANAGEMENT: Prepare the database interaction
# SessionLocal is a factory that produces new Session objects.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

# Helper function to get a new session using a context manager
def get_session():
    return SessionLocal()

# --- START CRUD OPERATIONS ---

print("--- 1. CREATE Operation (C) ---")
# C: Creating a new record (Persistence)
with get_session() as session:
    # 1a. Instantiate the Python object (Data exists only in memory)
    new_book = Book(title="The Theory of Everything", author="Dr. A. Scientist")
    print(f"Status: New object created in memory: {new_book}")
    
    # 1b. Add the object to the session (it is now pending)
    session.add(new_book)
    print("Status: Object added to session (pending commit).")
    
    # 1c. Commit the transaction to save the changes permanently to the database
    session.commit()
    
    # The object now has its primary key assigned after the commit
    print(f"Result: Book successfully created and persisted. ID: {new_book.id}") 

print("\n--- 2. READ Operation (R) ---")
# R: Reading records (Querying)
with get_session() as session:
    # 2a. Construct a SELECT statement to retrieve all books
    # We use select(Book) to indicate we want to retrieve Book objects
    statement = select(Book)
    
    # 2b. Execute the statement and fetch the results
    # session.scalars executes the query and returns the ORM objects directly
    all_books = session.scalars(statement).all()
    
    print(f"Result: Retrieved {len(all_books)} book(s) from the database.")
    for book in all_books:
        print(f"- Found: {book}")
        
    # Store the ID of the created book for Update/Delete later
    book_to_modify_id = all_books[0].id if all_books else None

if book_to_modify_id:
    print(f"\n--- 3. UPDATE Operation (U) ---")
    # U: Updating an existing record
    with get_session() as session:
        # 3a. Retrieve the specific object we want to change using .get()
        # .get() is highly efficient for fetching by Primary Key
        book_to_update = session.get(Book, book_to_modify_id)
        
        if book_to_update:
            original_title = book_to_update.title
            
            # 3b. Modify the Python object's attributes
            book_to_update.title = "The Revised Theory of Everything"
            print(f"Status: Title changed in memory from '{original_title}' to '{book_to_update.title}'")
            
            # 3c. Commit the session. SQLAlchemy detects the change automatically (Dirty Tracking).
            session.commit()
            print("Result: Change committed successfully to the database.")

    # Verification Read
    with get_session() as session:
        verified_book = session.get(Book, book_to_modify_id)
        print(f"Verification Check: Title is now: '{verified_book.title}'")


    print(f"\n--- 4. DELETE Operation (D) ---")
    # D: Deleting a record
    with get_session() as session:
        # 4a. Retrieve the specific object
        book_to_delete = session.get(Book, book_to_modify_id)
        
        if book_to_delete:
            # 4b. Mark the object for deletion
            session.delete(book_to_delete)
            print(f"Status: Marked book ID {book_to_delete.id} ('{book_to_delete.title}') for deletion.")
            
            # 4c. Commit the transaction to execute the deletion
            session.commit()
            print("Result: Book deleted successfully from the database.")

    # Final Verification Read
    print("\n--- Final Verification ---")
    with get_session() as session:
        # Check if the record still exists
        remaining_books = session.scalars(select(Book)).all()
        
        if not remaining_books:
            print("Database check: Record successfully deleted. No books remaining.")
        else:
            print(f"Database check: ERROR - Remaining books found: {remaining_books}")
