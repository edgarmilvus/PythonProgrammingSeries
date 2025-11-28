
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

# Filename: project_tracker.py
import json
import os
from typing import List, Dict, Any

# --- Configuration ---
# Define the persistent storage file name
DATA_FILE = "project_data.json"

def load_tasks(filepath: str) -> List[Dict[str, Any]]:
    """
    Loads task data from a JSON file.
    Handles common errors like file not found, empty files, and corrupt JSON.
    """
    if not os.path.exists(filepath):
        print(f"[{filepath}] not found. Starting with an empty task list.")
        return []

    try:
        # Use the 'with' statement (Pythonic context manager) for safe file handling
        with open(filepath, 'r', encoding='utf-8') as f:
            # Read the entire file content first
            content = f.read().strip()
            
            # Check for empty file content before attempting deserialization
            if not content:
                print(f"[{filepath}] is empty. Initializing list.")
                return []
            
            # Deserialization: JSON string (content) -> Python object (list of dicts)
            # json.loads() is used here because we read the string content first
            return json.loads(content)
            
    except json.JSONDecodeError:
        # Catches errors if the file content is not valid JSON syntax
        print(f"Error: Corrupt JSON data found in {filepath}. Returning empty list.")
        return []
    except IOError as e:
        # Catches general I/O errors (e.g., permission denied)
        print(f"File reading error: {e}")
        return []

def save_tasks(filepath: str, tasks: List[Dict[str, Any]]):
    """
    Saves the current list of tasks back to the JSON file.
    """
    try:
        # Open file in write mode ('w')
        with open(filepath, 'w', encoding='utf-8') as f:
            # Serialization: Python object -> JSON string, written directly to the file stream
            # json.dump() is preferred over json.dumps() + f.write() for direct file operations.
            # indent=4 ensures the output JSON is nicely formatted and human-readable.
            json.dump(tasks, f, indent=4)
        print(f"\nSuccessfully saved {len(tasks)} tasks to {filepath}.")
    except IOError as e:
        print(f"Error saving data: {e}")

def add_new_task(tasks: List[Dict[str, Any]], title: str, priority: str) -> int:
    """
    Creates a new task dictionary, assigns a sequential ID, and appends it.
    """
    # Determine the next sequential ID based on existing tasks
    next_id = 1
    if tasks:
        # Pythonic use of a generator expression with max() for efficiency
        next_id = max(task.get('id', 0) for task in tasks) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "status": "Pending",
        "priority": priority
    }
    tasks.append(new_task)
    print(f"Added Task ID {next_id}: '{title}' ({priority})")
    return next_id

def display_tasks(tasks: List[Dict[str, Any]]):
    """
    Prints the current task list in a formatted, readable way.
    """
    if not tasks:
        print("\n--- Task List is Empty ---")
        return

    print("\n--- Current Project Tasks ---")
    # Iterate through the Python list of dictionaries
    for task in tasks:
        # Use f-string formatting for alignment and clarity
        print(f"[{task['id']:<3}] {task['title']:<40} | Status: {task['status']:<10} | Priority: {task['priority']}")
    print("-" * 70)


def main():
    """Main execution flow for the project tracker application."""
    print("--- Project Tracker Initializing ---")
    
    # 1. Load existing data (Deserialization step)
    project_tasks = load_tasks(DATA_FILE)

    # 2. Display current state
    display_tasks(project_tasks)

    # 3. Modify the data (Application Logic manipulation in memory)
    print("\n--- Processing Updates ---")
    add_new_task(project_tasks, "Implement API endpoint for user authentication", "High")
    add_new_task(project_tasks, "Document Chapter 19 outline", "High")
    add_new_task(project_tasks, "Review dependency license compliance", "Medium")

    # 4. Display updated state
    display_tasks(project_tasks)

    # 5. Save the modified data (Serialization step)
    save_tasks(DATA_FILE, project_tasks)

if __name__ == "__main__":
    main()
