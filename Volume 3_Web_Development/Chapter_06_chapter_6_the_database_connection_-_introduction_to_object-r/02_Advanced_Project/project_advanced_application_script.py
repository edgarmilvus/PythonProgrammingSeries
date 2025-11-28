
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

import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import and_, func # func is used implicitly for date comparison

# --- 1. Database and ORM Setup ---

# Use an in-memory SQLite database for demonstration speed and portability
DATABASE_URL = "sqlite:///:memory:"
# Create the Engine; setting echo=False suppresses the raw SQL output
Engine = create_engine(DATABASE_URL, echo=False) 
# Base class used to define mapped classes (the foundation of the ORM)
Base = declarative_base()
# Session factory used to create individual sessions for database interaction
Session = sessionmaker(bind=Engine)

# --- 2. Model Definition (The Relational Mapping) ---

class ProjectTask(Base):
    """
    Maps the 'tasks' table structure to a Python class.
    Each class attribute corresponds to a database column.
    """
    __tablename__ = 'tasks'

    # Primary Key: Unique identifier for each task
    id = Column(Integer, primary_key=True)
    # Task title, limited to 100 characters and cannot be null
    title = Column(String(100), nullable=False)
    # Target completion date (using DateTime for full compatibility)
    due_date = Column(Date, default=datetime.date.today)
    # Boolean flag indicating task completion status
    is_complete = Column(Boolean, default=False)
    # Timestamp for when the record was created
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        """Standard representation method for debugging."""
        status = "Complete" if self.is_complete else "Pending"
        return f"<Task(id={self.id}, title='{self.title[:25]}...', Status={status})>"

# --- 3. Core Utility Functions (ORM-based CRUD) ---

def initialize_database():
    """Creates the table structure based on the Base metadata."""
    # This translates the Python class definition into DDL (CREATE TABLE SQL)
    Base.metadata.create_all(Engine)
    print("Database initialized and 'tasks' table created.")

def add_task(session, title, due_date_str):
    """Creates and persists a new task record using a date string."""
    try:
        # Parse the input string into a datetime.date object using standard format
        due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
        new_task = ProjectTask(title=title, due_date=due_date)
        
        # Stage the object for insertion (Unit of Work)
        session.add(new_task)
        # Execute the INSERT statement and persist the changes
        session.commit()
        print(f" [+] Task added: '{title}' (Due: {due_date})")
    except ValueError:
        session.rollback()
        print(" [!] Error: Invalid date format. Use YYYY-MM-DD.")
    except Exception as e:
        session.rollback()
        print(f" [!] An unexpected error occurred: {e}")

def query_overdue_pending_tasks(session):
    """Reads tasks that are past due and not yet completed."""
    today = datetime.date.today()
    
    # Complex query demonstrating ORM filter capabilities (solving impedance mismatch)
    # We filter for records where two conditions MUST be met (logical AND)
    overdue_tasks = session.query(ProjectTask).filter(
        and_(
            ProjectTask.is_complete == False, # Condition 1: Must be pending
            ProjectTask.due_date < today      # Condition 2: Due date must be in the past
        )
    ).order_by(ProjectTask.due_date.desc()).all()
    
    return overdue_tasks

def mark_task_complete(session, task_id):
    """Fetches a task by ID and updates its completion status."""
    # Read operation: Fetch the object by its primary key
    task = session.query(ProjectTask).get(task_id)
    
    if task:
        # Update operation: Modify the Python object attribute
        task.is_complete = True
        # Commit persists the tracked change (generates an UPDATE SQL statement)
        session.commit()
        print(f" [*] Task ID {task_id} marked as complete: {task.title}")
    else:
        print(f" [!] Task ID {task_id} not found for update.")

def display_all_tasks(session):
    """Reads and displays all tasks ordered by due date."""
    print("\n--- Current Task List ---")
    # Read operation: Query all records, ordered by due date
    tasks = session.query(ProjectTask).order_by(ProjectTask.due_date).all()
    
    if not tasks:
        print(" (No tasks currently in the database.)")
        return
        
    for task in tasks:
        status = "DONE" if task.is_complete else "PENDING"
        due = task.due_date.strftime('%Y-%m-%d')
        print(f" ID {task.id:<2} | Status: {status:<7} | Due: {due} | Title: {task.title}")
    print("-------------------------\n")


# --- 4. Execution Flow and Demonstration ---

if __name__ == "__main__":
    initialize_database()

    # 1. Instantiate the session object
    session = Session()

    # 2. Populate initial data (Create operations)
    print("\n--- Step 1: Data Creation (C) ---")
    # Set dates relative to today to ensure one task is overdue for the demo
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    next_week = (datetime.date.today() + datetime.timedelta(weeks=1)).strftime('%Y-%m-%d')
    
    add_task(session, "Finalize Q3 Budget Report", yesterday) # Overdue for demo
    add_task(session, "Review Chapter 6 ORM Code", tomorrow)
    add_task(session, "Deploy Backend Service v1.0", next_week)
    
    display_all_tasks(session)
    
    # 3. Complex Query and Filtering (Read operations)
    print("\n--- Step 2: Querying Overdue Tasks (R) ---")
    overdue = query_overdue_pending_tasks(session)
    
    if overdue:
        print(f"Found {len(overdue)} overdue and pending task(s):")
        for task in overdue:
            print(f" [!] CRITICAL: {task.title} (Due: {task.due_date})")
    else:
         print("No overdue tasks found.")

    # 4. Update the status of a task (Update operation)
    print("\n--- Step 3: Updating and Re-querying (U) ---")
    # Assuming ID 2 is 'Review Chapter 6 ORM Code'
    mark_task_complete(session, 2)
    
    display_all_tasks(session)

    # 5. Clean up the session connection
    session.close()
    print("\nDemonstration complete. Session closed.")
