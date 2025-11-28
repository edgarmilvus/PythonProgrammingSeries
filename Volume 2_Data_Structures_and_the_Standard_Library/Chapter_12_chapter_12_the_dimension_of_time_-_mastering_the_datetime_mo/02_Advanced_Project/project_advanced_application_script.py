
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
from datetime import timedelta
from collections import namedtuple

# --- Configuration and Data ---

# Define the expected format for input date strings
DATE_FORMAT = "%Y-%m-%d"
# Define the threshold (in days) for a milestone to be considered "Due Soon"
DUE_SOON_THRESHOLD_DAYS = 7

# Use namedtuple for structured, readable, and immutable data storage
Milestone = namedtuple('Milestone', ['name', 'deadline_str'])

# Input data simulating a project plan
RAW_PROJECT_DATA = [
    Milestone("Project Kickoff", "2023-01-05"),
    Milestone("Phase 1 Completion", "2023-03-15"),
    Milestone("Midpoint Review", "2023-05-20"),
    Milestone("Beta Launch", "2023-06-25"),
    Milestone("Final Documentation", "2024-01-10"), # Future date
    Milestone("Client Signoff", "2024-04-01")      # Future date
]

# --- Core Functions ---

def parse_milestone_dates(raw_data: list[Milestone], date_format: str) -> list:
    """
    Converts raw string deadlines into datetime objects using strptime.
    Returns a list of tuples: (name, datetime_object).
    """
    parsed_milestones = []
    for m in raw_data:
        try:
            # CRITICAL: Use strptime to convert the string into a datetime object
            deadline_dt = datetime.datetime.strptime(m.deadline_str, date_format).date()
            parsed_milestones.append((m.name, deadline_dt))
        except ValueError as e:
            print(f"Error parsing date for '{m.name}': {e}. Skipping.")
    return parsed_milestones

def get_project_start_date(parsed_milestones: list) -> datetime.date:
    """
    Finds the earliest date among all milestones to determine the project start.
    """
    # Use the min() function on the list of datetime objects
    if not parsed_milestones:
        return datetime.date.today()
    
    # Extract only the date objects for comparison
    dates = [item[1] for item in parsed_milestones]
    return min(dates)

def analyze_milestone(name: str, deadline: datetime.date, today: datetime.date) -> tuple:
    """
    Calculates the timedelta and determines the status of a single milestone.
    Returns: (time_remaining_str, status_label)
    """
    # Calculate the difference, resulting in a timedelta object
    time_remaining: timedelta = deadline - today
    
    # Determine Status based on the sign and magnitude of the timedelta
    if time_remaining.days < 0:
        status = "LATE"
        # Display time as absolute days overdue
        display_time = f"{abs(time_remaining.days)} days overdue"
    elif time_remaining.days <= DUE_SOON_THRESHOLD_DAYS:
        status = "DUE SOON"
        display_time = f"{time_remaining.days} days remaining"
    else:
        status = "ON TRACK"
        display_time = f"{time_remaining.days} days remaining"
        
    return display_time, status

def generate_report(parsed_milestones: list, project_start_date: datetime.date):
    """
    Generates and prints the final formatted project status report.
    """
    today = datetime.date.today()
    
    # Calculate total duration since project start
    project_duration: timedelta = today - project_start_date
    
    # --- Report Header ---
    print("\n" + "="*70)
    print("PROJECT MILESTONE STATUS REPORT")
    print(f"Report Date: {today.strftime('%Y-%m-%d %H:%M')}")
    print(f"Project Start: {project_start_date.strftime('%B %d, %Y')}")
    print(f"Total Project Duration: {project_duration.days} days elapsed")
    print("="*70)
    
    # --- Milestone Detail Loop ---
    print(f"{'STATUS':<12}{'MILESTONE':<30}{'DEADLINE':<15}{'TIME REMAINING':<20}")
    print("-" * 70)
    
    for name, deadline_dt in parsed_milestones:
        # Perform analysis for each milestone
        time_display, status_label = analyze_milestone(name, deadline_dt, today)
        
        # Format the deadline date for display using strftime
        formatted_deadline = deadline_dt.strftime("%b %d, %y")
        
        print(f"{status_label:<12}{name:<30}{formatted_deadline:<15}{time_display:<20}")
        
    print("-" * 70)

# --- Execution ---

if __name__ == "__main__":
    # 1. Convert raw strings to datetime objects
    processed_data = parse_milestone_dates(RAW_PROJECT_DATA, DATE_FORMAT)
    
    # 2. Determine the project start date
    start_date = get_project_start_date(processed_data)
    
    # 3. Generate and display the final report
    generate_report(processed_data, start_date)
