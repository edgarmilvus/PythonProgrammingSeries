
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

# The central data store for all contacts.
# Key: Contact Name (string)
# Value: Contact Record (tuple containing phone and email)
CONTACT_DB = {}

def add_contact(name: str, phone: str, email: str):
    """
    Adds a new contact record to the CONTACT_DB.
    Uses a tuple to ensure the record structure is fixed and immutable.
    """
    # 1. Create the standardized record using a tuple.
    # Tuples are chosen here for their immutability, signaling that
    # phone and email are fixed components of this specific record instance.
    record = (phone, email)
    
    # 2. Store the record in the dictionary using the name as the key.
    # Dictionary assignment is efficient (O(1) average time complexity).
    CONTACT_DB[name] = record
    print(f"[SUCCESS] Contact added: {name}")

def display_contact(name: str):
    """
    Retrieves and displays a single contact's details by name.
    """
    # Check if the name exists in the dictionary keys.
    if name in CONTACT_DB:
        # Retrieve the tuple value associated with the key.
        contact_record = CONTACT_DB[name]
        
        # Unpack the tuple into descriptive variables.
        # This is clean and readable, leveraging tuple unpacking.
        phone, email = contact_record
        
        print(f"\n--- Contact Details for {name} ---")
        print(f"Phone Number: {phone}")
        print(f"Email Address: {email}")
        print("-----------------------------------")
    else:
        # Handle the case where the key (name) is not found.
        print(f"[ERROR] Contact '{name}' not found in the database.")

def list_all_contacts():
    """
    Iterates through the entire dictionary and displays all stored contacts.
    """
    print("\n=== COMPLETE CONTACT DIRECTORY ===")
    if not CONTACT_DB:
        print("The database is currently empty.")
        return

    # Use .items() to efficiently iterate over both keys (names) and values (records).
    for name, record_tuple in CONTACT_DB.items():
        # Unpack the tuple again for display formatting.
        phone, email = record_tuple
        print(f"| Name: {name:<20} | Phone: {phone:<12} | Email: {email}")
    print("==================================")

# --- Execution Demonstration ---

# 1. Adding initial contacts
add_contact("Alice Wonderland", "555-1001", "alice@wonder.net")
add_contact("The Mad Hatter", "555-0303", "madhatter@tea.com")
add_contact("Cheshire Cat", "555-9999", "cat@grin.org")

# 2. Displaying a specific contact
display_contact("Alice Wonderland")

# 3. Attempting to display a contact that does not exist
display_contact("Queen of Hearts")

# 4. Listing the entire database contents
list_all_contacts()
