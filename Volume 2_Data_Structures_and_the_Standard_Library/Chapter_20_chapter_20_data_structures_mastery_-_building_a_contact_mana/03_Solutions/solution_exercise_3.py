
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

# Source File: solution_exercise_3.py
# Description: Solution for Exercise 3
# ==========================================

# Setup the CMS data structure
contacts = {
    "Alice Smith": {"phone": "1234567890", "email": "alice@example.com", "address": "101 Main St"},
    "Bob Johnson": {"phone": "0987654321", "email": "bob@work.net", "address": "202 Side Ave"}
}

def add_contact(contacts_dict: dict, name: str, phone: str, email: str, address: str) -> bool:
    """
    Requirement 1: Adds a contact with validation checks for name and phone.
    Returns True if added, False otherwise.
    """
    # Validation 1: Name must be non-empty
    if not name or len(name.strip()) == 0:
        print("Error: Name cannot be empty.")
        return False
    
    # Validation 2: Phone number must contain only digits
    if not phone.isdigit():
        print("Error: Phone number must contain only digits.")
        return False

    # Add contact if validation passes
    contacts_dict[name] = {
        "phone": phone,
        "email": email,
        "address": address
    }
    print(f"SUCCESS: Contact '{name}' added/updated.")
    return True


def delete_contact(contacts_dict: dict, name: str) -> bool:
    """
    Requirement 2: Deletes a contact and returns True/False based on success.
    """
    if name in contacts_dict:
        del contacts_dict[name]
        print(f"SUCCESS: Contact '{name}' deleted.")
        return True
    else:
        print(f"FAILURE: Contact '{name}' not found.")
        return False


def export_contacts_summary(contacts_dict: dict) -> list[tuple]:
    """
    Requirement 3: Extracts Name and Email into a standardized list of tuples.
    """
    summary_list = []
    
    # Iterate through the dictionary keys (Name) and values (nested dictionary)
    for name, data in contacts_dict.items():
        # Package the name and email into an immutable tuple
        summary_list.append((name, data.get('email', 'N/A')))
        
    return summary_list

# --- Testing and Menu Integration (Requirement 4) ---
print("\n--- CMS Robustness and Reporting Test ---")
add_contact(contacts, "Charlie Brown", "5551112222", "charlie@peanuts.com", "303 School Rd")
add_contact(contacts, "Invalid User", "abc12345", "fail@test.com", "N/A") # Fails validation
add_contact(contacts, "", "1234567890", "empty@name.com", "N/A") # Fails validation

print("\n--- Deletion Test ---")
delete_contact(contacts, "Bob Johnson")
delete_contact(contacts, "Non Existent")

print("\n--- Reporting (Requirement 4) ---")
summary = export_contacts_summary(contacts)

print("Exported Contacts Summary (List of Tuples):")
for entry in summary:
    print(entry)

# Example of Menu Integration (Conceptual)
# if user_choice == '4':
#     report = export_contacts_summary(contacts)
#     print(report)
