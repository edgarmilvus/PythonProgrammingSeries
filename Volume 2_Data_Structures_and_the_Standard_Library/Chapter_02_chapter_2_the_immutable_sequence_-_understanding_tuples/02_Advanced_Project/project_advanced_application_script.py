
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
from collections import namedtuple 

# --- 1. Define the Structured Data Type using namedtuple ---
# AuditRecord is an immutable sequence where elements can be accessed by name.
# Fields: (Record ID, Item Name, Unit Price, Quantity Sold, Audit Status)
AuditRecord = namedtuple("AuditRecord", 
                         ["record_id", "item_name", "unit_price", "quantity", "status"])

# --- 2. Input Data (Raw, simple tuples) ---
# This list simulates raw data pulled from a source, which may contain errors 
# or inconsistencies (e.g., negative prices, structural errors).
RAW_TRANSACTIONS = [
    (1001, "Server RAM Module", 150.75, 5, "COMPLETE"),
    (1002, "Fiber Optic Cable", 25.00, 12, "COMPLETE"),
    (1003, "Power Supply Unit", -80.00, 3, "ERROR_PRICE"), # Invalid price detected later
    (1004, "Network Switch (48p)", 450.99, 1, "PENDING"),
    (1005, "Patch Panel (Cat 6)", 15.50, 10, "COMPLETE"),
    (1006, "Cooling Fan", 5.00, 0, "COMPLETE"), 
    (1007, "KVM Switch", 300.00, 2, "COMPLETE"),
    (1008, "Missing Data", 10.00), # Structural error: too few elements
    (1009, "Negative Qty Test", 100.00, -5, "PENDING"), # Invalid quantity detected later
]

# --- 3. Processing and Validation Functions ---

def validate_and_structure_record(raw_tuple):
    """
    Takes a raw tuple, unpacks it, performs basic validation checks,
    and returns a structured AuditRecord namedtuple or None if invalid structure.
    """
    try:
        # Critical step: Unpacking the raw input tuple into named variables.
        # If the input tuple length is not exactly 5, this raises a ValueError.
        r_id, name, price, qty, status = raw_tuple
        
        # Validation 1: Check for positive price (critical for financial data)
        if price <= 0.0:
            print(f"Audit Warning: Record {r_id} has non-positive price ({price}). Marking as ERROR.")
            # We update the status variable *before* creating the immutable record
            status = "ERROR_PRICE"
            
        # Validation 2: Check for non-negative quantity
        if qty < 0:
            print(f"Audit Warning: Record {r_id} has negative quantity ({qty}). Marking as ERROR.")
            status = "ERROR_QTY"
            
        # Create and return the immutable namedtuple. 
        # Once this object is created, its attributes (r_id, name, price, etc.) cannot be changed.
        return AuditRecord(r_id, name, price, qty, status)
        
    except ValueError as e:
        # Catches cases where the raw tuple does not have exactly 5 elements (structural error)
        print(f"Structural Error: Malformed tuple input (expected 5 elements): {raw_tuple}. Details: {e}")
        return None

def calculate_total_audited_value(audited_records):
    """
    Calculates the total monetary value of all successfully completed records.
    Iterates over a sequence of namedtuples, accessing elements by name for clarity.
    """
    total_value = 0.0
    completed_count = 0
    
    for record in audited_records:
        # Accessing elements by name (readability benefit of namedtuple)
        if record.status == "COMPLETE":
            # Calculation: Price * Quantity
            transaction_value = record.unit_price * record.quantity
            total_value += transaction_value
            completed_count += 1
            
    return total_value, completed_count

# --- 4. Main Execution Block ---

def run_supply_chain_audit(raw_data):
    """
    Main function to execute the audit process flow.
    """
    print("--- Starting Supply Chain Transaction Audit ---")
    
    audited_data = [] # Temporary list to collect the structured namedtuples
    error_count = 0
    
    # Phase 1: Structure and Validate all records
    for raw_record in raw_data:
        structured_record = validate_and_structure_record(raw_record)
        
        if structured_record:
            # Check the status assigned during validation
            if structured_record.status.startswith("ERROR"):
                error_count += 1
            
            audited_data.append(structured_record)
        else:
            error_count += 1 # Count structural errors too

    print(f"\nPhase 1 Complete: {len(audited_data)} records structured. {error_count} errors/warnings detected.")
    
    # Phase 2: Analysis and Metrics
    total_value, completed_count = calculate_total_audited_value(audited_data)
    
    # Phase 3: Reporting
    print("\n--- Audit Summary Report ---")
    print(f"Total Raw Records Received: {len(raw_data)}")
    print(f"Structured Records (including errors): {len(audited_data)}")
    print(f"Records Marked as COMPLETE: {completed_count}")
    print(f"Total Audited Value (COMPLETE records only): ${total_value:,.2f}")
    
    # Demonstrating tuple access flexibility
    if audited_data:
        first_record = audited_data[0]
        print(f"\nVerification Check (Record ID {first_record.record_id}):")
        # Access by index (standard tuple behavior)
        print(f"Item Name (Index 1): {first_record[1]}") 
        # Access by attribute name (namedtuple benefit)
        print(f"Unit Price (Attribute): ${first_record.unit_price:,.2f}")
        
    print("--- Audit Concluded ---")
    
    # Return the final structured data as an immutable sequence (tuple of namedtuples)
    return tuple(audited_data) 

if __name__ == "__main__":
    final_audit_data = run_supply_chain_audit(RAW_TRANSACTIONS)
    # The final_audit_data is now ready for secure storage or transmission.
