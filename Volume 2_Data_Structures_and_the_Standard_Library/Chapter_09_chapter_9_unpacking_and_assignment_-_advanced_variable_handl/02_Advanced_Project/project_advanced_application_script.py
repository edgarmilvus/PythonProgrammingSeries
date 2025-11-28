
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
from typing import List, Tuple, Any, Dict

# Define the structured data set. Each tuple represents a transaction record.
# The length varies, demonstrating the need for extended unpacking.
TRANSACTION_DATA: List[Tuple[Any, ...]] = [
    (1001, 450.50, "Completed", "Online", "Standard"),
    (1002, 12.99, "Pending"),
    (1003, 9800.00, "Failed", "LargeTransfer", "FraudReview", "Note: Contact customer"),
    (1004, 25.00, "Completed"),
    (1005, 150.75, "Completed", "InStore"),
    (1006, 50.00, "Refunded", "Error: 504", "Note: System issue"),
    (1007, 200.00, "Completed", "Online", "Promo: SUMMER20"),
    (1008, 75.25, "Pending", "MobileApp"),
]

def process_transaction_record(record: Tuple[Any, ...]) -> Dict[str, Any] | None:
    """
    Processes a single transaction record using extended unpacking.

    The first three elements are fixed (ID, Amount, Status).
    All subsequent elements are captured into the 'metadata' list.
    """
    if len(record) < 3:
        # Minimum required fields are ID, Amount, Status
        print(f"Warning: Skipping malformed record (too short): {record}", file=sys.stderr)
        return None

    # CRITICAL USE OF EXTENDED UNPACKING:
    # Captures the first three elements explicitly, and bundles the rest into metadata.
    try:
        transaction_id, amount, status, *metadata = record
    except ValueError as e:
        # This usually only triggers if the record is exactly 0, 1, or 2 items long
        # but serves as robust error handling.
        print(f"Error during required unpacking for record {record}: {e}", file=sys.stderr)
        return None

    metadata_count = len(metadata)

    # Categorization logic based on the presence of optional metadata
    if metadata_count == 0:
        category = "Simple"
    elif metadata_count <= 2:
        category = "Standard"
    else:
        # Records with 3 or more tags are flagged for review
        category = "Complex/Flagged"

    return {
        "id": transaction_id,
        "amount": amount,
        "status": status,
        "category": category,
        "metadata": metadata,
        "metadata_count": metadata_count
    }

def generate_financial_report(data_set: List[Tuple[Any, ...]]):
    """
    Iterates through the data set, processes records, and generates a summary.
    Demonstrates basic unpacking and variable swapping.
    """
    processed_records = []
    total_transactions = 0
    total_amount = 0.0

    print("--- Financial Record Processor: Dynamic Unpacking Log ---")

    for record in data_set:
        processed_data = process_transaction_record(record)
        total_transactions += 1

        if processed_data:
            processed_records.append(processed_data)
            total_amount += processed_data['amount']

            # Demonstration of unpacking a dictionary's values view for selective access
            # The dictionary keys are ordered (id, amount, status, category, metadata, metadata_count)
            # CRITICAL USE OF UNDERSCORE (_) for ignoring unwanted fields
            # We only need the ID, Category, and Metadata Count for this log line.
            # Note: This relies on Python 3.7+ dictionary insertion order preservation.
            record_id, _, _, category, _, meta_count = processed_data.values()

            print(f"[{category:15}] ID: {record_id} | Status: {processed_data['status']:10} | Tags Captured: {meta_count}")

    print("\n" + "="*50)
    print("--- Summary Report ---")
    print(f"Total Transactions Attempted: {total_transactions}")
    print(f"Successfully Processed Records: {len(processed_records)}")
    print(f"Grand Total Amount: ${total_amount:,.2f}")
    print("="*50)

    # Calculate category totals
    standard_count = len([p for p in processed_records if p['category'] == 'Standard'])
    complex_count = len([p for p in processed_records if p['category'] == 'Complex/Flagged'])
    simple_count = len([p for p in processed_records if p['category'] == 'Simple'])

    print(f"Simple Transactions: {simple_count}")
    print(f"Standard Transactions: {standard_count}")
    print(f"Complex/Flagged Transactions: {complex_count}")

    # Further demonstration: Efficiently swapping variables based on a condition
    # Imagine we need to report the highest and lowest non-simple category counts.
    highest_priority_count = standard_count
    lowest_priority_count = complex_count

    if standard_count < complex_count:
        # CRITICAL USE OF SIMULTANEOUS ASSIGNMENT (VARIABLE SWAPPING)
        highest_priority_count, lowest_priority_count = lowest_priority_count, highest_priority_count
        print("\n[Action: Standard and Complex counts swapped due to higher volume of complex transactions.]")

    print(f"Highest Volume Non-Simple Category Count: {highest_priority_count}")
    print(f"Lowest Volume Non-Simple Category Count: {lowest_priority_count}")


if __name__ == "__main__":
    generate_financial_report(TRANSACTION_DATA)
