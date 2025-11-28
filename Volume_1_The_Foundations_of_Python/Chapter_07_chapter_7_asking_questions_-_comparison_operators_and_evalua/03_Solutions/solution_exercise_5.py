
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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

# Exercise 7.4.5 Setup: The Maintenance Scheduler

# 1. Define Variables
machine_status = 'Normal'
hours_run = 550
days_since_inspection = 35

# 2. Define Thresholds
HOURS_THRESHOLD = 500
DAYS_THRESHOLD = 30
CRITICAL_STATUS = 'Critical'

# 3. Check Critical Status (Path A)
is_critical = (machine_status == CRITICAL_STATUS)  # 'Normal' == 'Critical' -> False

# 4. Check Overdue Status (Path B - Compound AND)
hours_exceeded = (hours_run > HOURS_THRESHOLD)        # 550 > 500 -> True
days_exceeded = (days_since_inspection > DAYS_THRESHOLD)  # 35 > 30 -> True
is_overdue = (hours_exceeded and days_exceeded)       # True and True -> True

# 5. Determine Final Requirement (Path A OR Path B)
# Maintenance is required if it is critical OR if it is overdue.
maintenance_required = is_critical or is_overdue

# 6. Print Result
print(f"Machine Status: {machine_status}")
print(f"Hours Run: {hours_run}, Days Since Inspection: {days_since_inspection}")
print("-" * 30)
print(f"Is Critical: {is_critical}")
print(f"Is Overdue (Hours AND Days): {is_overdue}")
print(f"Maintenance Required: {maintenance_required}")
