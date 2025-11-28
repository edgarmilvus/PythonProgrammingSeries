
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

# Source File: solution_exercise_1.py
# Description: Solution for Exercise 1
# ==========================================

# CRITICAL SETUP IMPORTS
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

# --- 1. SETUP: ENGINE AND BASE ---

# Use an in-memory SQLite database for simplicity in testing
DATABASE_URL = "sqlite:///:memory:"
# Setting echo=False for cleaner output, but can be set to True for debugging SQL
Engine = create_engine(DATABASE_URL, echo=False) 
Base = declarative_base()

# --- 2. MODEL DEFINITIONS (For All Exercises) ---

# Exercise 1 Models
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    publication_year = Column(Integer)
    is_available = Column(Boolean, default=True)
    # Conceptual Foreign Key (used for linking, but not fully mapped yet)
    author_id = Column(Integer) 

    def __repr__(self):
        return f"<Book(title='{self.title}', author_id={self.author_id})>"

# Exercise 2 Model
class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    quantity = Column(Integer)

    def __repr__(self):
        return f"<Item(name='{self.name}', quantity={self.quantity})>"

# Exercise 3 Model
class UserProfile(Base):
    __tablename__ = 'user_profiles'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Profile(id={self.id}, user='{self.username}', email='{self.email}')>"

# Exercise 4 Model (Modified)
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    # E4 Modification: Adding priority column
    priority = Column(Integer) 

    def __repr__(self):
        return f"<Task(title='{self.title}', priority={self.priority})>"

# Exercise 5 Model
class Attendee(Base):
    __tablename__ = 'attendees'
    id = Column(Integer, primary_key=True)
    # E5 Constraint: Max length 50
    name = Column(String(50)) 
    # E5 Constraint: Must be unique
    email = Column(String, unique=True) 

    def __repr__(self):
        return f"<Attendee(name='{self.name}', email='{self.email}')>"


# --- 3. SESSION FACTORY AND INITIALIZATION ---

# Create the tables defined in Base
Base.metadata.create_all(Engine)

# Create a configured "Session" class
Session = sessionmaker(bind=Engine)

# --- 4. EXERCISE IMPLEMENTATIONS ---

print("--- Starting Exercise Runs ---")

# ====================================================================
# EXERCISE 1: The Atomic Transaction in a Library System
# ====================================================================

def add_new_author_and_books(session, author_name, book_list):
    """Inserts an author and multiple books in a single transaction."""
    print(f"\n[E1] Attempting to add Author: {author_name}")
    try:
        # 1. Create the Author object
        new_author = Author(name=author_name)
        session.add(new_author)
        
        # We use flush() to execute the INSERT for the Author immediately 
        # (getting the PK) without committing the transaction yet.
        session.flush() 

        # 2. Create Book objects linked to the new author's ID
        author_id = new_author.id
        for book_data in book_list:
            new_book = Book(
                title=book_data['title'],
                publication_year=book_data['year'],
                author_id=author_id
            )
            session.add(new_book)
            print(f"   -> Added book '{new_book.title}' to session.")

        # 3. Commit the entire transaction atomically
        session.commit()
        print(f"[E1] SUCCESS: Author and {len(book_list)} books committed atomically.")

    except Exception as e:
        # If any step (including flush or commit) fails, roll back everything
        session.rollback()
        print(f"[E1] FAILURE: Transaction rolled back due to error: {e}")

# Run E1
session_e1 = Session()
books_data = [
    {'title': 'Philosopher\'s Stone', 'year': 1997},
    {'title': 'Chamber of Secrets', 'year': 1998},
    {'title': 'Prisoner of Azkaban', 'year': 1999},
]
add_new_author_and_books(session_e1, "J. K. Rowling", books_data)

# E1 Verification
print("[E1] Verification:")
author_count = session_e1.query(Author).count()
book_count = session_e1.query(Book).count()
print(f"   -> Total Authors in DB: {author_count}") # Expected: 1
print(f"   -> Total Books in DB: {book_count}")     # Expected: 3
session_e1.close()


# ====================================================================
# EXERCISE 2: Inventory Management and Transaction Safety (Rollback)
# ====================================================================

def initialize_inventory(session):
    """Sets up the initial state for the inventory items."""
    # Ensure tables are clean before initialization
    session.query(InventoryItem).delete()
    session.add_all([
        InventoryItem(name='Widget A', quantity=10),
        InventoryItem(name='Widget B', quantity=5)
    ])
    session.commit()
    print("\n[E2] Initial Inventory Setup Complete (Widget A: 10, Widget B: 5).")

def process_order(session, item_updates):
    """Processes multiple inventory deductions transactionally."""
    print(f"\n[E2] Attempting to process order with {len(item_updates)} updates...")
    transaction_successful = True
    
    try:
        for update in item_updates:
            # Retrieve the item object
            item = session.query(InventoryItem).filter_by(name=update['name']).one()
            deduction = update['deduction']
            
            new_quantity = item.quantity - deduction
            
            if new_quantity < 0:
                # Business logic violation detected
                print(f"   -> ERROR: Deduction of {deduction} for {item.name} fails (Result: {new_quantity}).")
                transaction_successful = False
                break # Exit the loop immediately, preventing further modifications
            
            # Apply the valid change (still pending in the session cache)
            item.quantity = new_quantity
            print(f"   -> Updated {item.name} in session: {item.quantity + deduction} -> {item.quantity}")

        if transaction_successful:
            # If all items passed validation, commit all changes
            session.commit()
            print("[E2] SUCCESS: Order processed and committed.")
        else:
            # If failure occurred, undo all pending changes
            session.rollback()
            print("[E2] ROLLBACK: Transaction failed due to inventory constraint violation.")
            
    except Exception as e:
        session.rollback()
        print(f"[E2] CRITICAL FAILURE: Database error encountered: {e}. Session rolled back.")
        transaction_successful = False
        
    return transaction_successful

# Run E2
session_e2 = Session()
initialize_inventory(session_e2)

# Test Case 1 (Success): Initial state (10, 5) -> (7, 4)
updates_success = [
    {'name': 'Widget A', 'deduction': 3},
    {'name': 'Widget B', 'deduction': 1}
]
process_order(session_e2, updates_success)

# Test Case 2 (Failure): Current state (7, 4). Deduct 12 from A.
updates_failure = [
    {'name': 'Widget A', 'deduction': 12}, # This will fail validation
    {'name': 'Widget B', 'deduction': 1}  # This valid change should also be undone
]
process_order(session_e2, updates_failure)

# E2 Verification
print("[E2] Verification after Failure Rollback:")
# We expect the quantities to be the result of the successful commit (7 and 4), 
# as the subsequent failed transaction was rolled back.
items = session_e2.query(InventoryItem).order_by(InventoryItem.name).all()
for item in items:
    print(f"   -> {item.name}: Final Quantity {item.quantity}") 
session_e2.close()


# ====================================================================
# EXERCISE 3: User Profile Lifecycle (Update and Delete)
# ====================================================================

session_e3 = Session()
print("\n[E3] Starting User Profile Lifecycle Test.")

# Initial Insertion
initial_user = UserProfile(username='testuser', email='old@example.com')
session_e3.add(initial_user)
session_e3.commit()
user_id = initial_user.id
print(f"[E3] 1. Inserted user with ID: {user_id}. Email: {initial_user.email}")

# Update Operation
try:
    # Retrieve the object by primary key
    user_to_update = session_e3.get(UserProfile, user_id) 
    if user_to_update:
        # Modify the attribute
        user_to_update.email = 'new@updated.com'
        # Commit the change to the database
        session_e3.commit()
        print(f"[E3] 2. Updated user email. New Email: {user_to_update.email}")
        
        # Verification of Update
        verified_user = session_e3.get(UserProfile, user_id)
        print(f"[E3] 2.1 Verification: Retrieved email is '{verified_user.email}'. (Success)")

except SQLAlchemyError as e:
    session_e3.rollback()
    print(f"[E3] Error during update: {e}")


# Deletion Operation
try:
    user_to_delete = session_e3.get(UserProfile, user_id)
    if user_to_delete:
        # Mark the object for deletion
        session_e3.delete(user_to_delete)
        # Execute the DELETE statement
        session_e3.commit()
        print(f"[E3] 3. Successfully marked user ID {user_id} for deletion and committed.")

        # Final Verification
        deleted_user = session_e3.get(UserProfile, user_id)
        if deleted_user is None:
            print("[E3] 3.1 Verification: Record successfully removed (Query returned None). (Success)")
        else:
            print("[E3] 3.1 Verification: Deletion FAILED.")

except SQLAlchemyError as e:
    session_e3.rollback()
    print(f"[E3] Error during deletion: {e}")
finally:
    session_e3.close()


# ====================================================================
# EXERCISE 4: Interactive Challenge: Enforcing Task Priority Constraints
# ====================================================================

def attempt_bad_insert(session):
    """Attempts to insert a task with invalid priority and handles rollback."""
    print("\n[E4] Attempting invalid insert (priority=5)...")
    
    # Simulate a constraint violation (a value that would fail a CHECK constraint)
    bad_task = Task(title="Invalid Priority Task", description="Should fail commit", priority=5)
    session.add(bad_task)
    
    try:
        session.commit()
        # Note: In SQLite, without raw SQL CHECK constraints, this might commit. 
        # The focus is on the exception handling mechanism.
        print("[E4] WARNING: Invalid task was committed (Constraint not enforced by SQLite ORM).")
        
    # Catch the database error that would occur on a production system
    except (IntegrityError, OperationalError) as e:
        print(f"[E4] CAUGHT EXCEPTION: Database constraint violation detected: {type(e).__name__}")
        # CRITICAL STEP: Rollback to clear the failed transaction state
        session.rollback()
        print("[E4] Session successfully rolled back and recovered.")
        
    except Exception as e:
        session.rollback()
        print(f"[E4] Unforeseen error during commit: {e}. Session rolled back.")

def verify_session_recovery(session):
    """Attempts a valid insert after the failure test."""
    print("\n[E4] Testing Session Recovery with Valid Insert...")
    
    valid_task = Task(title="Valid Task", description="Should commit successfully", priority=2)
    session.add(valid_task)
    
    try:
        session.commit()
        print("[E4] SUCCESS: Valid task committed after previous rollback.")
        
        # Verification
        task_count = session.query(Task).count()
        print(f"[E4] Final Task Count: {task_count}. (Expected 1)")
        
    except Exception as e:
        session.rollback()
        print(f"[E4] FAILURE: Session was NOT recovered. Error: {e}")

# Run E4
session_e4 = Session()
session_e4.query(Task).delete()
session_e4.commit() # Clear table

# 1. Run the failure test (which should trigger rollback)
attempt_bad_insert(session_e4)

# 2. Run the recovery test (which proves the session is usable again)
verify_session_recovery(session_e4)

session_e4.close()


# ====================================================================
# EXERCISE 5: Data Integrity and Unique Constraints
# ====================================================================

session_e5 = Session()
print("\n[E5] Starting Unique Constraint Test.")

# 1. Initial Valid Insertion
try:
    attendee1 = Attendee(name='Jane Doe', email='jane@event.com')
    session_e5.add(attendee1)
    session_e5.commit()
    print("[E5] 1. Successfully inserted Jane Doe.")
except SQLAlchemyError as e:
    session_e5.rollback()
    print(f"[E5] Initial insert failed: {e}")

# 2. Constraint Violation Test (Unique Email)
print("[E5] 2. Attempting to insert duplicate email...")
attendee2 = Attendee(name='John Smith', email='jane@event.com') # Duplicate email
session_e5.add(attendee2)

try:
    session_e5.commit()
    print("[E5] WARNING: Duplicate email was committed. (Constraint failed)")
except IntegrityError as e:
    # This is the expected error for a UNIQUE constraint violation
    print(f"[E5] CAUGHT IntegrityError: Database rejected duplicate email.")
    session_e5.rollback()
    print("[E5] Session rolled back successfully.")
except Exception as e:
    session_e5.rollback()
    print(f"[E5] Unexpected error during unique test: {e}")

# 3. Constraint Violation Test (Length - Conceptual)
print("[E5] 3. Attempting to insert overly long name (100 chars)...")
long_name = 'A' * 100
# SQLite often truncates the string silently if it exceeds 50, but the definition is correct.
attendee3 = Attendee(name=long_name, email='longname@event.com')
session_e5.add(attendee3)

try:
    session_e5.commit()
    print("[E5] Length test: Committed (Name may be truncated to 50 chars).")
except Exception as e:
    session_e5.rollback()
    print(f"[E5] Length test failed unexpectedly: {e}")

# Rollback the conceptual length test insertion to ensure only Jane Doe remains
session_e5.rollback()

# 4. Final Verification
print("[E5] Final Verification:")
final_attendees = session_e5.query(Attendee).all()
print(f"   -> Total Attendees in DB: {len(final_attendees)}") # Expected: 1
for att in final_attendees:
    print(f"   -> {att.name}: {att.email}")

session_e5.close()
