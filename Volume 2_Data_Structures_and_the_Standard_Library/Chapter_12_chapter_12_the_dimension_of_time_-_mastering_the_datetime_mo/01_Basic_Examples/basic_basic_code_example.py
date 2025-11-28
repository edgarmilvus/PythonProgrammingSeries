
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

# datetime_fundamentals.py

# 1. Import the necessary classes from the datetime module
from datetime import date, datetime, timedelta

# --- Part 1: Working with Dates (The 'date' object) ---

# 2. Define a fixed historical date (e.g., the start of a project: Jan 1, 2023)
project_start_date = date(2023, 1, 1)
print(f"Project Start Date: {project_start_date}")

# 3. Get today's date using a class method
today = date.today()
print(f"Today's Date: {today}")

# 4. Calculate the duration between the two dates (results in a timedelta object)
duration_since_start = today - project_start_date
print(f"Duration since project start (raw): {duration_since_start}")

# 5. Access the duration in days
days_elapsed = duration_since_start.days
print(f"Total days elapsed: {days_elapsed}")


# --- Part 2: Working with Specific Moments (The 'datetime' object) ---

# 6. Get the current precise date and time
now = datetime.now()
print(f"\n[Current Time] Raw datetime object: {now}")


# --- Part 3: Working with Durations (The 'timedelta' object) ---

# 7. Define a specific duration (30 days, 5 hours, and 15 minutes)
# This represents the length of a task plus review time
task_duration = timedelta(days=30, hours=5, minutes=15)
print(f"Task Duration (timedelta): {task_duration}")

# 8. Calculate the exact future moment by adding the duration to 'now'
# datetime + timedelta = new datetime
completion_moment = now + task_duration
print(f"Completion Moment: {completion_moment}")

# 9. Demonstrate comparison logic
is_completion_in_future = completion_moment > now
print(f"Is the completion moment later than 'now'? {is_completion_in_future}")

# 10. Accessing individual components of a datetime object
print(f"Completion Year: {completion_moment.year}")
print(f"Completion Hour: {completion_moment.hour}")
