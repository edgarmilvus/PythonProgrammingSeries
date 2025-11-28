
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

from datetime import datetime, date, timedelta, timezone

# =================================================================
# EXERCISE 1: The Project Deadline Tracker
# =================================================================

print("--- Exercise 1: Project Deadline Tracker ---")

# 1. Determine the current date
current_date = date.today()

# 2. Define durations using timedelta
project_duration = timedelta(days=125)
# Three weeks prior is 3 * 7 = 21 days
review_duration = timedelta(weeks=3)

# 3. Calculate final deadline (Current Date + Project Duration)
final_deadline = current_date + project_duration

# 4. Calculate milestone review date (Deadline - Review Duration)
milestone_review_date = final_deadline - review_duration

# 5. Define the required output format: YYYY-MM-DD (DayName)
date_format = "%Y-%m-%d (%A)"

# Print results using strftime()
print(f"Current Date:            {current_date.strftime(date_format)}")
print(f"Final Project Deadline:  {final_deadline.strftime(date_format)}")
print(f"Milestone Review Date:   {milestone_review_date.strftime(date_format)}")
print("-" * 40)


# =================================================================
# EXERCISE 2: Standardizing Log Data Formatting
# =================================================================

print("--- Exercise 2: Standardizing Log Data ---")

entry_a_str = "2024-May-15 10:45:12.345678"
entry_b_str = "05/24/2024 16:01"

# Define the target output format (ISO 8601 standard with microseconds)
iso_format = "%Y-%m-%d %H:%M:%S.%f"

# 1. Parse Entry A: YYYY-AbbreviatedMonth-DD HH:MM:SS.microseconds
format_a = "%Y-%b-%d %H:%M:%S.%f"
dt_a = datetime.strptime(entry_a_str, format_a)

# 2. Parse Entry B: MM/DD/YYYY HH:MM (Note: seconds/microseconds default to 0)
format_b = "%m/%d/%Y %H:%M"
dt_b = datetime.strptime(entry_b_str, format_b)

# 3. Format and print standardized output
print(f"Original A: {entry_a_str}")
print(f"Standard A: {dt_a.strftime(iso_format)}")
print(f"Original B: {entry_b_str}")
print(f"Standard B: {dt_b.strftime(iso_format)}")
print("-" * 40)


# =================================================================
# EXERCISE 3: Shift Duration and Overtime Calculation
# =================================================================

print("--- Exercise 3: Shift Duration Analysis ---")

# Define an arbitrary date to create full datetime objects
today = date.today()

# 1. Define clock-in and clock-out times as datetime objects
clock_in = datetime(today.year, today.month, today.day, 8, 45, 0)   # 08:45:00
clock_out = datetime(today.year, today.month, today.day, 17, 15, 30) # 17:15:30

# 2. Calculate total shift duration (datetime subtraction yields timedelta)
shift_duration = clock_out - clock_in

# 3. Define standard workday duration (8 hours)
standard_workday = timedelta(hours=8)

# 4. Calculate overtime/undertime
overtime = shift_duration - standard_workday

# Helper function to format timedelta output for readability
def format_timedelta(td):
    """Formats a timedelta object into H hours, M minutes, S seconds."""
    # Check if the duration is negative (undertime)
    sign = "-" if td.total_seconds() < 0 else ""
    total_seconds = int(abs(td.total_seconds()))
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{sign}{hours} hours, {minutes} minutes, {seconds} seconds"

print(f"Shift Clock In:      {clock_in.strftime('%H:%M:%S')}")
print(f"Shift Clock Out:     {clock_out.strftime('%H:%M:%S')}")
print(f"Total Shift Duration: {format_timedelta(shift_duration)}")
print(f"Standard Duration:   {format_timedelta(standard_workday)}")

# 5. Print the overtime/undertime result
if overtime.total_seconds() > 0:
    print(f"Overtime Worked:     {format_timedelta(overtime)}")
elif overtime.total_seconds() < 0:
    # Display undertime as a positive duration with a negative indicator
    print(f"Undertime Worked:    {format_timedelta(overtime)}")
else:
    print("Exact Standard Shift Worked.")
print("-" * 40)


# =================================================================
# EXERCISE 4: Interactive Challenge - Time Zone Aware Logging
# =================================================================

print("--- Exercise 4: Time Zone Aware Logging ---")

# 1. Define the assumed local time zone (UTC-5 hours offset)
LOCAL_TZ = timezone(timedelta(hours=-5), name='UTC-5')

# Simple storage mechanism (simulating a database/log file)
LOG_STORAGE = []

# 3. Function to log an event, converting local time to UTC
def log_event(message):
    # Get current time, explicitly making it aware of the local TZ
    # This is the cleanest way to create an aware object reflecting local time
    local_aware_time = datetime.now(tz=LOCAL_TZ)
    
    # Convert the local aware time to UTC aware time for standardized storage
    utc_aware_time = local_aware_time.astimezone(timezone.utc)
    
    log_entry = {
        'message': message,
        # Store the aware UTC datetime object
        'utc_timestamp': utc_aware_time
    }
    LOG_STORAGE.append(log_entry)
    print(f"[LOGGED] Message: '{message}'")
    # Display the stored UTC time
    print(f"         Stored UTC Time: {utc_aware_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    return log_entry

# 5. Function to display the log entry, converting UTC back to local time
def display_log(log_entry):
    utc_time = log_entry['utc_timestamp']
    message = log_entry['message']
    
    # Convert the stored UTC time back to the assumed local time zone for the user
    local_display_time = utc_time.astimezone(LOCAL_TZ)
    
    print(f"\n[DISPLAY] Event: {message}")
    print(f"          (DB UTC Time): {utc_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"          (Local UTC-5 Time): {local_display_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

# 6. Demonstration
log1 = log_event("Server starting up.")
log2 = log_event("User attempted login.")

print("\n--- Retrieving and Displaying Logs ---")
display_log(log1)
display_log(log2)
print("-" * 40)
