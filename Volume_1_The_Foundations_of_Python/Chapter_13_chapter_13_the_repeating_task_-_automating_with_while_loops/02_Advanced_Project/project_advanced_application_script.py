
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

# task_manager.py - A Simple Command-Line Task Manager using while Loops

# -----------------
# 1. Setup and Global State
# -----------------
tasks = [] # The main list to store tasks (strings)
status_pending = "[ ]"
status_done = "[X]"

def display_menu():
    """Prints the main interactive menu options."""
    print("\n--- Task Manager Menu ---")
    print("1. Add New Task")
    print("2. View All Tasks")
    print("3. Mark Task as Complete")
    print("4. Clear All Completed Tasks")
    print("Q. Quit Application")
    print("-------------------------")

def add_task(task_list):
    """Allows the user to input and add a new pending task."""
    print("\n--- Add New Task ---")
    
    # Inner while loop for input validation and task entry
    while True:
        new_task = input("Enter task description (or type 'cancel'): ").strip()
        
        if new_task.lower() == 'cancel':
            print("Task addition cancelled.")
            return # Exit the function
            
        if len(new_task) > 5:
            # Prepend the pending status indicator
            task_list.append(f"{status_pending} {new_task}")
            print(f"Task added: '{new_task}'")
            break # Successfully added, break the inner while loop
        else:
            print("Error: Task description must be longer than 5 characters.")
            continue # Loop back for valid input

def view_tasks(task_list):
    """Displays all tasks with their corresponding index."""
    if not task_list:
        print("\n[INFO] Your task list is currently empty.")
        return

    print("\n--- Current Task List ---")
    for index, task in enumerate(task_list):
        # Display index (starting from 1 for user readability) and the task string
        print(f"{index + 1}. {task}")
    print("-------------------------")

def complete_task(task_list):
    """Allows the user to mark a task as done using its index."""
    if not task_list:
        print("\n[INFO] No tasks to complete.")
        return

    view_tasks(task_list) # Show the list first

    # Inner while loop for index validation
    while True:
        try:
            choice = input("Enter the number of the task to complete (or '0' to cancel): ")
            
            if choice == '0':
                print("Completion cancelled.")
                return

            task_index = int(choice) - 1 # Convert user input (1-based) to list index (0-based)
            
            # Check if the index is valid
            if 0 <= task_index < len(task_list):
                old_task = task_list[task_index]
                
                # Check if already completed using string replacement logic
                if old_task.startswith(status_done):
                    print("Task already marked as complete.")
                    break
                
                # Update the task status marker
                updated_task = old_task.replace(status_pending, status_done, 1)
                task_list[task_index] = updated_task
                print(f"Task {task_index + 1} marked as complete.")
                break # Success, break the inner while loop
            else:
                print(f"Invalid number. Please enter a number between 1 and {len(task_list)}.")
                continue # Loop back for valid index input

        except ValueError:
            print("Invalid input. Please enter a numeric task index.")
            continue # Loop back for valid type input

def clear_completed(task_list):
    """Removes all tasks marked with the 'done' status."""
    initial_count = len(task_list)
    
    # We use a while loop here to manually iterate and build a new list of pending items.
    pending_tasks = []
    i = 0
    while i < len(task_list):
        task = task_list[i]
        if task.startswith(status_pending):
            pending_tasks.append(task)
        i += 1 # Crucial state management: incrementing the counter

    tasks[:] = pending_tasks # Replace the global list content
    removed_count = initial_count - len(tasks)
    
    if removed_count > 0:
        print(f"\nSuccessfully cleared {removed_count} completed tasks.")
    else:
        print("\nNo completed tasks were found to clear.")


# -----------------
# 2. Main Application Loop (The heart of the chapter)
# -----------------
print("Welcome to the Python Command-Line Task Manager.")

# The primary control loop, runs indefinitely until 'Q' is chosen.
while True:
    display_menu()
    
    # Prompt for the user's choice
    user_choice = input("Enter your selection (1-4 or Q): ").strip().upper()
    
    # Check for the termination condition
    if user_choice == 'Q':
        print("\nThank you for using the Task Manager. Goodbye!")
        break # Exits the main while True loop
    
    # Handle the main menu actions
    elif user_choice == '1':
        add_task(tasks)
    elif user_choice == '2':
        view_tasks(tasks)
    elif user_choice == '3':
        complete_task(tasks)
    elif user_choice == '4':
        clear_completed(tasks)
    else:
        # If input is invalid, the loop continues to the next iteration
        print("\n[ERROR] Invalid selection. Please choose from the menu options.")
        continue # Skip the rest of the loop body and jump back to the start (display_menu)
