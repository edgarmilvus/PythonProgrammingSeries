
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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

# app.py (Comprehensive Solution Script)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Import necessary exception for rollback handling (E2)
from sqlalchemy.exc import IntegrityError
from config import Config
import os

# --- 1. Initial Setup and Configuration ---
db = SQLAlchemy()

def create_app():
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

# --- 2. Exercise 1 & 5: Model Definition and Augmentation ---

class Publisher(db.Model):
    """Model definition for the Publisher table (E1)."""
    id = db.Column(db.Integer, primary_key=True)
    # E1 Requirement: unique=True, nullable=False
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        """E1 Requirement: Representation method."""
        return f"<Publisher ID={self.id}, Name='{self.name}'>"

class Book(db.Model):
    """Model definition for the Book table (E1, E5)."""
    id = db.Column(db.Integer, primary_key=True)
    # E1 Requirement: nullable=False
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer)
    
    # E5 Augmentation: Adding the status column with a default value
    status = db.Column(db.String(20), default='Available', nullable=False)

    def __repr__(self):
        """E1 Requirement: Representation method."""
        return (f"<Book ID={self.id}, Title='{self.title}', Year={self.publication_year}, "
                f"Status='{self.status}'>")

# --- 3. CRUD Functions for Exercises 2, 3, 4, 5 ---

def setup_and_insert_data():
    """Handles E2 and E5 data insertion and database setup."""
    print("\n--- E2/E5: Data Insertion and Rollback Demonstration ---")
    
    # E5 Requirement 2: Drop and recreate tables for schema update
    db.drop_all()
    db.create_all()
    print("Database tables dropped and recreated (incorporating E5 status column).")

    # E2 Requirements 1, 2: Create objects
    p1 = Publisher(name='Penguin Classics')
    p2 = Publisher(name="O'Reilly Media")
    
    # Note: Status will default to 'Available' (E5)
    b1 = Book(title='Moby Dick', publication_year=1851)
    b2 = Book(title='The Pragmatic Programmer', publication_year=1999)
    b3 = Book(title='1984', publication_year=1949)

    try:
        # E2 Requirement 3, 4: Insertion and Commit
        db.session.add_all([p1, p2, b1, b2, b3])
        db.session.commit()
        print("Initial 5 records successfully committed.")

        # E2 Requirement 5: Test Rollback (Attempting duplicate unique name)
        p_duplicate = Publisher(name='Penguin Classics')
        db.session.add(p_duplicate)
        db.session.commit()
        
    except IntegrityError:
        # E2 Requirement 5: Rollback on error
        db.session.rollback()
        print("Integrity Error caught (Duplicate Publisher name). Session rolled back.")
        
    # E2 Requirement 6: Verification
    print(f"Current Publishers count: {Publisher.query.count()}")
    print(f"Current Books count: {Book.query.count()}")


def run_queries():
    """Handles E3: Advanced Querying and Filtering."""
    print("\n--- E3: Advanced Querying and Filtering (Read) ---")

    # E3 Query 1: Simple Filter (filter_by)
    def get_book_by_title(title):
        print(f"\nQuery 1: Searching for book titled '{title}'...")
        # .first() retrieves one object or None
        book = Book.query.filter_by(title=title).first()
        if book:
            print(f"Result: {book}")
        return book

    # E3 Query 2: Advanced Filtering (filter and like)
    def search_books_by_title_substring(search_term):
        print(f"\nQuery 2: Searching for books containing '{search_term}'...")
        # .like() requires model attribute expression
        books = Book.query.filter(Book.title.like(f'%{search_term}%')).all()
        print(f"Found {len(books)} matches:")
        for book in books:
            print(f"  - {book.title}")

    # E3 Query 3: Complex Criteria and Ordering
    def get_classic_books():
        print("\nQuery 3: Retrieving books published before 1950 (Descending Year)...")
        # Use comparison operator (<) and order_by()
        classics = (
            Book.query
            .filter(Book.publication_year < 1950)
            .order_by(Book.publication_year.desc())
            .all()
        )
        for book in classics:
            print(f"  - {book}")

    get_book_by_title('1984')
    search_books_by_title_substring('Programmer')
    get_classic_books()


def run_updates_and_deletes():
    """Handles E4: Update and Delete."""
    print("\n--- E4: Object Modification and Deletion (U & D) ---")

    # E4 Requirement 1: Update Operation
    moby_dick = Book.query.filter_by(title='Moby Dick').first()
    if moby_dick:
        print(f"Update Check: Before change: {moby_dick}")
        
        # Modify the object (SQLAlchemy tracks this change)
        moby_dick.publication_year = 1852
        
        # Commit the change (UPDATE statement is executed)
        db.session.commit()
        print(f"Update Check: After commit (Year changed to 1852): {moby_dick}")
    else:
        print("Book 'Moby Dick' not found for update.")

    # E4 Requirement 2: Deletion Operation
    oreilly = Publisher.query.filter_by(name="O'Reilly Media").first()
    if oreilly:
        print(f"\nPreparing to delete: {oreilly}")
        
        # Mark object for deletion
        db.session.delete(oreilly)
        db.session.commit()
        print("Deletion committed.")
        
        # Verification
        if Publisher.query.filter_by(name="O'Reilly Media").first() is None:
            print("Verification successful: O'Reilly Media is deleted.")
        else:
            print("Verification failed: Publisher still exists.")
    else:
        print("Publisher 'O'Reilly Media' not found for deletion.")


def archive_old_books(year_threshold):
    """Handles E5: Bulk Update Function."""
    print(f"\n--- E5 Interactive Challenge: Archiving Books before {year_threshold} ---")
    
    # E5 Requirement 4: Query all books published before the threshold
    old_books = Book.query.filter(Book.publication_year < year_threshold).all()
    
    if not old_books:
        print("No books found matching the archive criteria.")
        return

    print(f"Found {len(old_books)} books to archive.")
    
    # Iterate and modify attributes (Unit of Work tracks changes)
    for book in old_books:
        book.status = 'Archived'
        print(f"  -> Archiving: {book.title}")

    # E5 Requirement 4: Commit the batch update
    db.session.commit()
    print("Bulk update committed successfully.")

    # E5 Requirement 5: Verification
    print("\nVerification of all book statuses:")
    all_books = Book.query.all()
    for book in all_books:
        print(f"  {book.title} (Year: {book.publication_year}): Status -> {book.status}")


# --- 4. Execution Block ---

if __name__ == '__main__':
    app = create_app()
    
    # Running all exercises within the application context
    with app.app_context():
        
        # --- Run E1, E2, E5 Setup ---
        # This function sets up the tables and inserts the initial data.
        setup_and_insert_data() 
        
        # --- Run E3 Read Operations ---
        run_queries()
        
        # --- Run E4 Update and Delete Operations ---
        # This changes Moby Dick's year to 1852 and deletes O'Reilly Media.
        run_updates_and_deletes()
        
        # --- Run E5 Interactive Challenge ---
        # To ensure the archiving logic works as intended (Moby Dick 1851, 1984 1949), 
        # we must reset the data, as E4 modified Moby Dick's year to 1852 (which is > 1950).
        
        print("\n--- Resetting data for E5 final test (ensuring Moby Dick is 1851) ---")
        setup_and_insert_data()
        
        # Running E5 on the clean data (Moby Dick 1851 and 1984 1949 should be archived)
        archive_old_books(1950)
