
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

# 1. Initial Data: A list representing raw sign-ups (with duplicates)
initial_signups = [
    "Alice", "Bob", "Charlie", "Alice", "David", "Eve", "Bob", "Frank"
]

# 2. Creating the Set: Converting the list to a set to ensure uniqueness
# The set constructor automatically removes duplicate entries.
registered_attendees = set(initial_signups)

print(f"--- Registration Summary ---")
# Using the standard list length
print(f"Total sign-ups received (including duplicates): {len(initial_signups)}")
# Using the set length, which reflects the true number of individuals
print(f"Official unique attendee count: {len(registered_attendees)}")
print("-" * 20)

# 3. Membership Testing: Checking if a person is registered
new_applicant = "Charlie"
# Sets excel at the 'in' operation.
if new_applicant in registered_attendees:
    print(f"Check 1: '{new_applicant}' is already registered.")
else:
    print(f"Check 1: '{new_applicant}' needs to register.")

# 4. Adding a New Attendee
late_signup = "Grace"
# Use the .add() method to include a new, unique element.
registered_attendees.add(late_signup)
print(f"\nAction: Added '{late_signup}' to the roster.")

# 5. Attempting to Add a Duplicate (Idempotence Test)
registered_attendees.add("Alice") # This operation has no effect, as Alice is already present.
print(f"Action: Attempted to re-add 'Alice'. Set size remains unchanged.")

# 6. Removing an Attendee (Cancellation)
cancellation = "David"
if cancellation in registered_attendees:
    # Use the .remove() method to take an element out.
    registered_attendees.remove(cancellation)
    print(f"Action: Removed '{cancellation}' due to cancellation.")

# 7. Final State
print("\n--- Final Unique Attendee Roster ---")
# Note that the output order may not match the input order, as sets are unordered.
print(registered_attendees)
