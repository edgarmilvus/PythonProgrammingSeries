
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

import time
from collections import defaultdict, Counter, deque
from typing import Dict, List, Any, Tuple

# --- 1. Data Simulation Setup ---
def generate_simulated_logs() -> List[Dict[str, Any]]:
    """Generates a list of dictionaries simulating web traffic log entries."""
    
    # Define potential actions and pages for variation
    actions = ["VIEW", "LOGIN", "LOGOUT", "PURCHASE", "ERROR", "API_CALL"]
    pages = ["/home", "/product/A", "/product/B", "/checkout", "/support", "/dashboard"]
    statuses = [200, 404, 500, 302]
    
    log_data = []
    
    # Create 50 simulated log entries
    for i in range(50):
        user_id = f"User_{i % 10 + 1}"  # Simulate 10 unique users
        action = actions[i % len(actions)]
        page = pages[i % len(pages)]
        status = statuses[i % len(statuses)]
        
        # Introduce specific failure cases for deque tracking
        if action == "ERROR" and status == 500:
            status = 500 # Explicitly set status 500 for error tracking
        elif action == "LOGIN" and i % 7 == 0:
            status = 401 # Unauthorized login attempt
            
        timestamp = time.time() - (50 - i) # Simulate sequential time
        
        log_data.append({
            "timestamp": int(timestamp),
            "user_id": user_id,
            "action": action,
            "page": page,
            "status": status
        })
        
    return log_data

# --- 2. Core Processing Function ---
def process_logs(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Processes the log data using defaultdict, Counter, and deque.
    """
    
    # 2.1. Initialize Grouping Structure (defaultdict)
    # Groups all actions (list) under a specific user_id (key)
    user_activity: defaultdict[str, List[Dict[str, Any]]] = defaultdict(list)
    
    # 2.2. Initialize Counting Structure (Counter)
    # Tracks the frequency of page visits
    page_view_counts: Counter = Counter()
    
    # 2.3. Initialize Bounded Buffer (deque)
    # Stores the 5 most recent critical errors (e.g., Status 500 or 401)
    # maxlen=5 ensures automatic O(1) eviction of the oldest element
    recent_critical_errors: deque[Tuple[str, int, str]] = deque(maxlen=5)

    print(f"--- Processing {len(logs)} log entries... ---")
    
    # 2.4. Iterating and Populating Collections
    for entry in logs:
        user_id = entry['user_id']
        page = entry['page']
        status = entry['status']
        action = entry['action']
        
        # A. Grouping: Use defaultdict to append action details directly
        # If user_id doesn't exist, defaultdict creates the key and assigns an empty list
        user_activity[user_id].append({
            'action': action, 
            'page': page, 
            'status': status
        })
        
        # B. Counting: Use Counter to tally page views instantly
        # Counter handles the increment operation internally
        page_view_counts[page] += 1
        
        # C. Buffering: Check for critical errors (401 Unauthorized or 500 Server Error)
        if status in [401, 500]:
            error_details = (user_id, status, action)
            # Append to the deque. If maxlen is reached, the oldest element is automatically popped from the left.
            recent_critical_errors.append(error_details)
            
    return {
        "user_activity": user_activity,
        "page_views": page_view_counts,
        "critical_errors": recent_critical_errors
    }

# --- 3. Reporting Function ---
def display_report(results: Dict[str, Any]) -> None:
    """Formats and prints the analysis results."""
    
    print("\n" + "="*80)
    print("                 WEB TRAFFIC ANALYSIS REPORT")
    print("="*80 + "\n")

    # 3.1. Display Most Popular Pages (Using Counter's most_common method)
    print("1. TOP 5 MOST FREQUENTLY VISITED PAGES:")
    top_pages = results['page_views'].most_common(5)
    for page, count in top_pages:
        print(f"    - {page:<15}: {count} views")
    print("-" * 40)

    # 3.2. Display Recent Critical Errors (Using deque)
    print("\n2. 5 MOST RECENT CRITICAL ERRORS (LIFO Buffer):")
    # The deque naturally holds the most recent items due to maxlen constraint
    # We print them in the order they were added (oldest to newest in the buffer)
    if results['critical_errors']:
        for i, (user, status, action) in enumerate(results['critical_errors']):
            print(f"    {i+1}. [Status {status}] User {user} attempted {action}")
    else:
        print("    No critical errors recorded in the recent buffer.")
    print("-" * 40)

    # 3.3. Display User Activity Summary (Using defaultdict results)
    print("\n3. USER ACTIVITY SUMMARY:")
    
    # Sort users by activity count (demonstrating the structure of defaultdict output)
    sorted_users = sorted(
        results['user_activity'].items(), 
        key=lambda item: len(item[1]), 
        reverse=True
    )
    
    for user_id, actions in sorted_users[:3]:
        action_count = len(actions)
        # Use a temporary Counter to quickly summarize actions per user
        action_summary = Counter(a['action'] for a in actions)
        
        print(f"    > {user_id} ({action_count} total actions):")
        
        # Display the top 3 actions for this user
        for action, count in action_summary.most_common(3):
            print(f"        - {action}: {count}")
    print("="*80)


# --- 4. Main Execution ---
if __name__ == "__main__":
    
    # Generate the source data
    log_data = generate_simulated_logs()
    
    # Process the data using the specialized collections
    analysis_results = process_logs(log_data)
    
    # Output the final report
    display_report(analysis_results)

