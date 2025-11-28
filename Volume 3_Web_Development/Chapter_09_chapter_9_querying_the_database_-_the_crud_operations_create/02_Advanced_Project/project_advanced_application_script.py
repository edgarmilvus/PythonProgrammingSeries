
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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# --- 1. Initialization and Configuration ---

# Define the database file path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'task_manager.db')

app = Flask(__name__)
# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
# Disable tracking modification overhead
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- 2. Database Model Definition ---

class Task(db.Model):
    """Defines the structure for a Task item."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")
    status = db.Column(db.String(20), default='To Do') # e.g., 'To Do', 'In Progress', 'Done'
    priority = db.Column(db.Integer, default=5) # 1 (Highest) to 10 (Lowest)

    def __repr__(self):
        # A helpful representation for debugging
        return f'<Task {self.id}: {self.title} [{self.status}]>'

# --- 3. CRUD Operations Functions ---

def create_task(title, description, priority):
    """C: Creates a new Task and adds it to the session."""
    print(f"\n[CREATE] Attempting to create: {title}")
    try:
        new_task = Task(
            title=title,
            description=description,
            priority=priority
        )
        db.session.add(new_task)
        db.session.commit() # Persist the new object to the database
        print(f"   -> Success: Task ID {new_task.id} created.")
        return new_task
    except Exception as e:
        db.session.rollback() # Crucial rollback on failure
        print(f"   -> Error creating task: {e}")
        return None

def read_tasks(status=None, limit=5):
    """R: Reads and filters tasks based on status and returns a limited set."""
    print(f"\n[READ] Querying tasks (Status Filter: {status if status else 'All'})...")
    
    query = Task.query
    
    if status:
        # Apply filtering condition
        query = query.filter(Task.status == status)
        
    # Apply ordering and limiting
    tasks = query.order_by(Task.priority.asc(), Task.id.desc()).limit(limit).all()
    
    if not tasks:
        print("   -> No tasks found matching criteria.")
        return []
        
    print(f"   -> Found {len(tasks)} tasks.")
    for task in tasks:
        print(f"      - ID {task.id} (P:{task.priority}): {task.title} ({task.status})")
    return tasks

def update_task_status(task_id, new_status, new_priority=None):
    """U: Finds a task by ID and updates its status and optionally priority."""
    print(f"\n[UPDATE] Attempting to update Task ID: {task_id}")
    task = Task.query.get(task_id) # Primary key lookup (efficient)
    
    if task:
        old_status = task.status
        old_priority = task.priority
        
        task.status = new_status
        if new_priority is not None:
            task.priority = new_priority
            
        db.session.commit() # Commit the changes to the database
        print(f"   -> Success: Task ID {task_id} updated.")
        print(f"      Status: {old_status} -> {task.status}")
        if new_priority is not None:
             print(f"      Priority: {old_priority} -> {task.priority}")
        return task
    else:
        print(f"   -> Error: Task ID {task_id} not found.")
        return None

def delete_task(task_id):
    """D: Deletes a task record from the database."""
    print(f"\n[DELETE] Attempting to delete Task ID: {task_id}")
    task = Task.query.get(task_id)
    
    if task:
        db.session.delete(task)
        db.session.commit()
        print(f"   -> Success: Task ID {task_id} ('{task.title}') deleted.")
        return True
    else:
        print(f"   -> Error: Task ID {task_id} not found for deletion.")
        return False

# --- 4. Execution Block (Demonstration) ---

if __name__ == '__main__':
    # Context management ensures Flask environment is active for DB operations
    with app.app_context():
        # 4a. Setup: Drop and recreate tables for a clean start
        db.drop_all()
        db.create_all()
        print("\nDatabase initialized and tables created.")

        # 4b. CREATE Operations
        task1 = create_task("Design Database Schema", "Define relationships for users and tasks.", 1)
        task2 = create_task("Implement Frontend UI", "Build basic HTML structure for task viewing.", 8)
        task3 = create_task("Setup CI/CD Pipeline", "Configure Jenkins/GitHub Actions.", 3)
        task4 = create_task("Write Documentation", "Draft initial README and API specifications.", 2)
        
        # 4c. READ Operations (Initial State)
        read_tasks(limit=10)
        
        # 4d. UPDATE Operations
        # Task 1 is now in progress and its priority needs adjustment
        update_task_status(task1.id, 'In Progress', new_priority=1)
        # Task 3 is completed
        update_task_status(task3.id, 'Done')

        # 4e. READ Operations (Filtered and Ordered)
        read_tasks(status='In Progress', limit=1)
        read_tasks(status='Done', limit=10)
        
        # 4f. DELETE Operation
        # We decide to drop the documentation requirement for now
        delete_task(task4.id)

        # 4g. Final Verification Read
        print("\n[FINAL CHECK] Remaining tasks:")
        read_tasks(limit=10)
        
        # 4h. Example of Aggregation (Advanced Read)
        print("\n[AGGREGATION] Counting tasks by status:")
        status_counts = db.session.query(
            Task.status, func.count(Task.id).label('count')
        ).group_by(Task.status).all()
        
        for status, count in status_counts:
            print(f"   - Status '{status}': {count} tasks")
