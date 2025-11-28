
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

import sys

# --- Global Data Structure Initialization ---
# CONTACT_DB uses the Name (string) as the key for O(1) retrieval.
# The value is a tuple (Phone, Email, Category) for standardized, immutable records.
CONTACT_DB = {}
RECORD_FIELDS = ("Phone", "Email", "Category") # Defines the tuple structure metadata

# --- Helper Function ---
def get_input(prompt: str) -> str:
    """Standardizes user input handling."""
    return input(f"-> {prompt}: ").strip()

# --- Core CMS Operations ---

def add_contact(db: dict):
    """
    Prompts user for contact details and adds a new record to the database.
    Ensures uniqueness based on the contact name (the dictionary key).
    """
    print("\n--- Adding New Contact ---")
    name = get_input("Enter Contact Name (Unique Identifier)")
    if not name:
        print("[ERROR] Name cannot be empty.")
        return

    # Dictionary key lookup for O(1) existence check
    if name in db:
        print(f"[ERROR] Contact '{name}' already exists. Use a unique name.")
        return

    phone = get_input("Enter Phone Number")
    email = get_input("Enter Email Address")
    category = get_input("Enter Category (e.g., Work, Family, Vendor)")

    # Data Structure Application: Creation of the standardized tuple record
    contact_record = (phone, email, category)
    db[name] = contact_record
    print(f"\n[SUCCESS] Contact '{name}' added successfully.")

def view_all_contacts(db: dict):
    """
    Displays all contacts in the database, ordered alphabetically by name.
    Demonstrates tuple unpacking for clean display.
    """
    if not db:
        print("\n--- The Contact Database is currently empty. ---")
        return

    print("\n--- Comprehensive Contact List ---")
    # Sorting keys ensures a consistent, readable output order
    for name, record in sorted(db.items()):
        # Tuple unpacking: Assigning elements of the tuple to named variables
        phone, email, category = record
        print(f"Name: {name}")
        print(f"  {RECORD_FIELDS[0]}: {phone}")
        print(f"  {RECORD_FIELDS[1]}: {email}")
        print(f"  {RECORD_FIELDS[2]}: {category}")
        print("-" * 30)

def search_contact(db: dict):
    """
    Searches contacts by Name prefix or by exact Category match.
    Iterates through the dictionary values (tuples) to find matches.
    """
    query = get_input("Enter Name prefix or Category to search")
    if not query:
        print("[INFO] Search query cannot be empty.")
        return

    found_results = {}
    query_lower = query.lower()

    # Iterating over the entire dictionary to perform a value-based search
    for name, record in db.items():
        # Search Criterion 1: Name Prefix Match (using dictionary keys)
        if name.lower().startswith(query_lower):
            found_results[name] = record
            continue

        # Search Criterion 2: Category Match (using the third element of the tuple)
        category = record[2]
        if category.lower() == query_lower:
            found_results[name] = record

    if not found_results:
        print(f"\n[INFO] No contacts found matching '{query}'.")
        return

    print(f"\n--- Search Results for '{query}' ({len(found_results)} found) ---")
    for name, record in found_results.items():
        phone, email, category = record
        print(f"Name: {name} | Phone: {phone} | Email: {email} | Category: {category}")
    print("-" * 60)

def delete_contact(db: dict):
    """
    Deletes a contact using the name as the key.
    Leverages the speed of dictionary key deletion.
    """
    name_to_delete = get_input("Enter the Name of the contact to delete")
    
    # Efficient deletion using the 'del' keyword and key lookup
    if name_to_delete in db:
        del db[name_to_delete]
        print(f"\n[SUCCESS] Contact '{name_to_delete}' deleted.")
    else:
        print(f"\n[ERROR] Contact '{name_to_delete}' not found.")

# --- Main Execution Loop ---

def run_manager():
    """Manages the application flow and user interaction."""
    print("\n=======================================================")
    print("--- Python Data Structures Contact Manager V1.0 ---")
    print("=======================================================")
    
    while True:
        print("\n[Menu] 1: Add | 2: View All | 3: Search | 4: Delete | 5: Exit")
        choice = get_input("Select an option")

        if choice == '1':
            add_contact(CONTACT_DB)
        elif choice == '2':
            view_all_contacts(CONTACT_DB)
        elif choice == '3':
            search_contact(CONTACT_DB)
        elif choice == '4':
            delete_contact(CONTACT_DB)
        elif choice == '5':
            print("Exiting Contact Manager. Thank you for using the system!")
            sys.exit(0) # Use sys.exit for clean termination
        else:
            print("[WARNING] Invalid option selected. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    run_manager()
