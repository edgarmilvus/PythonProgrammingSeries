
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

# employee_performance_evaluator.py
# This script uses functions to modularize the process of evaluating employee performance metrics.

from collections import namedtuple

# --- 1. Data Structure Definition ---
# Using namedtuple enhances readability by allowing access to fields by name (e.g., employee.tasks_completed).
EmployeeRecord = namedtuple(
    "EmployeeRecord", 
    ["employee_id", "tasks_completed", "hours_worked", "quality_score", "days_absent"]
)

# --- 2. Core Utility Functions ---

def calculate_task_efficiency(tasks: int, hours: float) -> float:
    """
    Calculates the task completion rate (tasks per hour).
    
    This function takes two numerical inputs and returns a single float.
    
    :param tasks: Total number of tasks completed.
    :param hours: Total hours worked on those tasks.
    :return: The calculated efficiency rate (tasks/hour).
    """
    # Defensive check: Ensure we do not attempt division by zero.
    if hours <= 0:
        return 0.0
    
    # Calculate the rate and return the floating-point result.
    efficiency_rate = tasks / hours
    return efficiency_rate

def evaluate_quality_score(score: int) -> bool:
    """
    Determines if the quality score meets the 'Excellent' threshold (90+).
    
    This function is crucial as it returns a Boolean, essential for control flow.
    
    :param score: The employee's quality score (0-100).
    :return: True if score >= 90, False otherwise (a Boolean result).
    """
    # Pythonic approach: Direct comparison returns the required Boolean.
    is_excellent = score >= 90
    return is_excellent

# --- 3. Main Evaluation Function ---

def determine_promotion_eligibility(efficiency: float, quality_ok: bool, days_absent: int) -> tuple[str, bool]:
    """
    Determines overall promotion eligibility based on aggregated metrics.
    
    This function accepts outputs (float, Boolean) from other functions.

    :param efficiency: Task efficiency rate (tasks/hour).
    :param quality_ok: Boolean indicating if quality score was excellent.
    :param days_absent: Number of days the employee was absent.
    :return: A tuple containing (evaluation_summary_string, is_eligible_boolean).
    """
    
    # Define internal thresholds for easy modification and readability
    MIN_EFFICIENCY = 1.5
    MAX_ABSENCES = 3
    
    # Initialize state variables
    is_eligible = True
    summary = "Evaluation Summary:\n"
    
    # Check 1: Efficiency Requirement
    if efficiency < MIN_EFFICIENCY:
        is_eligible = False # Fail state
        summary += f"- Efficiency ({efficiency:.2f}) is below the required {MIN_EFFICIENCY:.1f} tasks/hour.\n"
    else:
        summary += f"- Efficiency ({efficiency:.2f}) meets the standard.\n"
        
    # Check 2: Quality Requirement (Relies directly on the Boolean input)
    if not quality_ok:
        is_eligible = False # Fail state
        summary += "- Quality score was not marked as excellent (below 90).\n"
    else:
        summary += "- Quality score is excellent.\n"

    # Check 3: Attendance Requirement
    if days_absent > MAX_ABSENCES:
        is_eligible = False # Fail state
        summary += f"- Attendance is poor (Exceeded {MAX_ABSENCES} days absent).\n"
    else:
        summary += "- Attendance is satisfactory.\n"
        
    # Final determination based on the cumulative 'is_eligible' flag
    if is_eligible:
        summary += "\n-> FINAL STATUS: Eligible for Promotion Review."
    else:
        summary += "\n-> FINAL STATUS: Not Eligible for Promotion Review."
        
    # Return the detailed summary and the final Boolean status
    return summary, is_eligible

# --- 4. Main Orchestration Function ---

def run_evaluation(employee: EmployeeRecord):
    """
    Orchestrates the entire evaluation process for a single employee record.
    This function demonstrates the calling sequence and data flow between defined functions.
    """
    print(f"--- Processing Employee ID: {employee.employee_id} ---")
    
    # Step 1: Calculate Efficiency (Function 1 call)
    efficiency_rate = calculate_task_efficiency(
        tasks=employee.tasks_completed, 
        hours=employee.hours_worked
    )
    
    # Step 2: Evaluate Quality (Function 2 call, returns a Boolean)
    is_quality_excellent = evaluate_quality_score(
        score=employee.quality_score
    )
    
    # Step 3: Determine Eligibility (Function 3 call, using results from Steps 1 & 2)
    evaluation_report, final_eligibility = determine_promotion_eligibility(
        efficiency=efficiency_rate,
        quality_ok=is_quality_excellent,
        days_absent=employee.days_absent
    )
    
    # Step 4: Output Results
    print(evaluation_report)
    print("-" * 40)
    print(f"Is {employee.employee_id} eligible? {final_eligibility}")
    print("=" * 40 + "\n")


# --- 5. Data Initialization and Script Entry Point ---

if __name__ == "__main__":
    # Create sample employee records using the structured namedtuple
    employee_data = [
        # Employee 1: Meets all criteria (Eligible)
        EmployeeRecord("E401", 180, 100.0, 95, 2),
        
        # Employee 2: Fails efficiency and attendance (Not Eligible)
        EmployeeRecord("E402", 100, 80.0, 92, 5),
        
        # Employee 3: Fails quality score (Not Eligible)
        EmployeeRecord("E403", 200, 110.0, 85, 1),
    ]
    
    # Loop through the data, calling the main orchestration function for each record.
    for record in employee_data:
        run_evaluation(record)
