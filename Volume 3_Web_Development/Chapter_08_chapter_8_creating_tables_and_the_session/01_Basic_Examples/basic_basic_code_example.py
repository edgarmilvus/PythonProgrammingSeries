
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

import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

# ----------------------------------------------------------------------
# 1. DATABASE SETUP AND MODEL DEFINITION
# ----------------------------------------------------------------------

# Define the base class for declarative class definitions.
# This Base class acts as a catalog for all defined models.
Base = declarative_base()

class Task(Base):
    # __tablename__ is mandatory and defines the name of the table in the database
    __tablename__ = 'tasks'

    # Define columns: SQLAlchemy maps these Python attributes to SQL columns
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    is_completed = Column(Boolean, default=False)

    def __repr__(self):
        # A useful representation method for printing objects cleanly
        status = "Completed" if self.is_completed else "Pending"
        return f"<Task(id={self.id}, description='{self.description[:30]}...', status='{status}')>"

# ----------------------------------------------------------------------
# 2. ENGINE AND METADATA CREATION
# ----------------------------------------------------------------------

# Use an in-memory SQLite database (data exists only while the script runs)
# The 'sqlite:///:memory:' connection string is standard for temporary databases.
DATABASE_URL = "sqlite:///:memory:"
# echo=True would print every generated SQL query, useful for debugging
engine = create_engine(DATABASE_URL, echo=False) 

# Create all defined tables in the database. 
# This command reads the metadata attached to the Base class (i.e., the Task class)
Base.metadata.create_all(engine)

# ----------------------------------------------------------------------
# 3. SESSION FACTORY SETUP
# ----------------------------------------------------------------------

# Configure the Session factory. This object will be used to create new sessions.
# We bind the factory to our created engine.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ----------------------------------------------------------------------
# 4. DATA INTERACTION (THE SESSION IN ACTION)
# ----------------------------------------------------------------------

# Step 1: Create a new transactional session instance
session = SessionLocal()

try:
    print("--- 4a. Adding New Data ---")
    
    # Instantiate Python objects (Transient State)
    task1 = Task(description="Finalize Chapter 8 draft and review examples.")
    task2 = Task(description="Schedule meeting with editor.", is_completed=True)

    # Add the objects to the session. They are now tracked (Pending State).
    session.add(task1)
    session.add(task2)
    
    print(f"Task 1 before commit (ID likely None or temporary): {task1}")

    # Commit the transaction: This sends the buffered changes to the database.
    # The session is now in Persistent State.
    session.commit()
    print("SUCCESS: Data committed to the database. IDs assigned.")
    print(f"Task 1 after commit (ID assigned): {task1}")

    # Step 2: Querying Data
    print("\n--- 4b. Retrieving Data ---")
    
    # Query all Task objects from the database using the session
    all_tasks = session.query(Task).all()
    
    print(f"Total tasks found: {len(all_tasks)}")
    for task in all_tasks:
        print(f"  > ID {task.id} | Status: {'DONE' if task.is_completed else 'TODO'} | Description: {task.description}")

    # Step 3: Updating Data
    print("\n--- 4c. Updating Data ---")
    
    # Retrieve a specific task by its primary key (ID 1)
    task_to_update = session.query(Task).get(1)
    
    if task_to_update:
        print(f"Task ID {task_to_update.id} status before update: {task_to_update.is_completed}")
        
        # Modify the attribute of the Python object
        task_to_update.is_completed = True 
        
        # We must commit again to persist this update to the database
        session.commit()
        print("SUCCESS: Task status updated and committed.")
        
        # Verification
        verified_task = session.query(Task).get(1)
        print(f"Verification Check: Task ID 1 is_completed={verified_task.is_completed}")

except Exception as e:
    # If any error occurs (e.g., connection lost, constraint violation), 
    # we must explicitly rollback to undo any partial changes.
    print(f"\nERROR DETECTED: {e}")
    session.rollback()

finally:
    # Crucial step: Always close the session to release resources and connections
    session.close()

print("\nScript finished. Session closed.")
