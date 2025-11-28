
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

import random
from collections import namedtuple
from datetime import date, timedelta

# --- 1. Data Definitions and Setup ---

# Define a structured data type for employees using namedtuple
# namedtuple provides readable, immutable structure for team members.
Employee = namedtuple('Employee', ['id', 'name', 'role'])

# List of employees available for weekly assignments
EMPLOYEE_POOL = [
    Employee(101, "Alice Johnson", "Dev"),
    Employee(102, "Bob Smith", "QA"),
    Employee(103, "Charlie Brown", "Dev"),
    Employee(104, "Diana Prince", "Architect"),
    Employee(105, "Ethan Hunt", "DevOps"),
    Employee(106, "Fiona Glenanne", "PM"),
    Employee(107, "George Kirk", "QA"),
    Employee(108, "Hannah Montana", "Dev"),
]

# List of critical tasks that must be assigned weekly
CRITICAL_TASKS = [
    "Database Migration Review",
    "Security Audit Preparation",
    "Client Demo Lead",
    "System Stress Testing",
]

# Set the seed for reproducible results (Crucial for testing/auditing)
# Using a fixed seed ensures that the same input always yields the same output.
random.seed(42)

# --- 2. Core Randomization Function ---

def generate_weekly_assignments(employees, tasks):
    """
    Selects a team using sampling, shuffles tasks, and chooses a backup.

    Args:
        employees (list): List of Employee namedtuples.
        tasks (list): List of strings representing tasks.

    Returns:
        tuple: (list of (name, task) assignments, backup_member namedtuple)
    """
    
    # 1. Determine required team size (must match the number of tasks)
    team_size = len(tasks)

    # 2. Use random.sample() to select unique team members without replacement
    # This guarantees that four distinct employees are chosen for the four tasks.
    primary_team = random.sample(employees, team_size)
    
    # 3. Create a mutable list of tasks for shuffling
    assignable_tasks = list(tasks)
    
    # 4. Use random.shuffle() to randomize the order of tasks IN PLACE
    # This ensures that the assignment of Task A vs. Task B is entirely random.
    random.shuffle(assignable_tasks)

    # 5. Combine selected members and shuffled tasks into final assignments
    weekly_assignments = []
    for i in range(team_size):
        assignment = (primary_team[i].name, assignable_tasks[i])
        weekly_assignments.append(assignment)

    # 6. Determine the remaining pool for backup selection
    # Collect names of selected members to filter the original pool efficiently
    selected_names = {p.name for p in primary_team}
    remaining_pool = [e for e in employees if e.name not in selected_names]

    # 7. Use random.choice() to select a single backup from the remaining pool
    # This guarantees the backup is not simultaneously assigned a primary task.
    backup_member = random.choice(remaining_pool)
    
    return weekly_assignments, backup_member

# --- 3. Execution and Reporting Setup ---

# Calculate the start date for the report (next Monday)
today = date.today()
# Calculate days until next Monday (Monday is day 0, Sunday is day 6)
# The % 7 handles wrapping, and the conditional handles the case if today is Monday.
days_until_monday = (7 - today.weekday()) % 7
if days_until_monday == 0:
     days_until_monday = 7 # If today is Monday, target next week
     
start_date = today + timedelta(days=days_until_monday)

# Generate the assignments
assignments, backup = generate_weekly_assignments(EMPLOYEE_POOL, CRITICAL_TASKS)

# --- 4. Output Presentation ---

print("-" * 75)
print(f"PROJECT MANAGEMENT ASSIGNMENT REPORT | Week Starting: {start_date.strftime('%Y-%m-%d')}")
print("-" * 75)
print("\n[ Primary Critical Task Assignments ]")

# Use random.randint() to assign a random priority score (1-10) for flavor
for name, task in assignments:
    # Generates an integer between 1 and 10, inclusive
    priority = random.randint(1, 10) 
    print(f"  > {name:<20} | Task: {task:<30} | Priority Score: {priority}")

print("\n[ Team Backup / On-Call ]")
# Use random.random() to simulate a readiness score (float 0.0 to 1.0)
# This adds a small, purely random metric to the report.
readiness_score = random.random()
print(f"  > {backup.name:<20} | Role: {backup.role:<10} | Readiness Factor: {readiness_score:.4f}")
print("-" * 75)
