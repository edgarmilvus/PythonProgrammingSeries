
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
import time
import random
from typing import Generator, Tuple, Dict

# --- Configuration ---
# Simulate a large dataset of half a million records
TOTAL_RECORDS = 500_000 
VALUE_THRESHOLD = 1000.00
TARGET_PRIORITY = "HIGH"

# --- 1. Data Simulation (Acts like reading a massive file line by line) ---

def simulate_data_stream(num_records: int) -> Generator[str, None, None]:
    """
    Generates raw transaction data strings.
    This function simulates reading lines from a very large CSV file, 
    yielding one line (string) at a time.
    """
    priorities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    for i in range(1, num_records + 1):
        # Simulate ID, Priority, and Value
        transaction_id = f"TX{i:06d}"
        priority = random.choice(priorities)
        # Generate random values between 50 and 5000
        value = round(random.uniform(50.00, 5000.00), 2)
        # Yield the raw string line (e.g., "TX000001,HIGH,1500.50")
        yield f"{transaction_id},{priority},{value}"

# --- 2. Supporting Function for Data Transformation ---

def parse_transaction(raw_line: str) -> Tuple[str, str, float]:
    """
    Parses a raw CSV line into a structured tuple (ID, Priority, Value).
    This function is called by the first generator expression.
    """
    try:
        parts = raw_line.strip().split(',')
        # Ensure value is converted to float for calculation
        return parts[0], parts[1], float(parts[2])
    except (ValueError, IndexError):
        # Handle malformed lines gracefully without crashing the stream
        print(f"Skipping malformed line: {raw_line}", file=sys.stderr)
        return "", "", 0.0 # Return empty data to be filtered out later

# --- 3. Main Processing Logic using Generator Expressions ---

def process_large_dataset(num_records: int, threshold: float, priority: str) -> float:
    """
    Orchestrates the data flow using multiple chained Generator Expressions 
    for lazy evaluation.
    """
    print(f"--- Starting Data Processing ({num_records:,} records) ---")

    # Step A: Create the raw data stream (Generator)
    # This is the source of the data, yielding strings upon request.
    raw_stream = simulate_data_stream(num_records)

    # Step B: Transformation Generator Expression (Lazy Map)
    # Syntax: ( expression for item in iterable )
    # This generator applies the parsing logic (map) but does not execute it yet.
    structured_data = (
        parse_transaction(line)
        for line in raw_stream
    )
    print("B. Structured Data Generator created (Lazy Parsing)")


    # Step C: Filtering Generator Expression (Lazy Filter)
    # This generator is chained immediately after the previous one.
    # It filters the structured data based on priority and value threshold.
    # We only extract the value (data[2]) for the final calculation.
    high_value_transactions = (
        data[2] # We only need the value (index 2)
        for data in structured_data
        if data[1] == priority and data[2] >= threshold
    )
    print(f"C. Filter Generator created (Target: {priority}, > ${threshold:,.2f})")

    # Step D: Aggregation (Consumption)
    # The built-in sum() function is the consumer. It pulls data through 
    # the entire pipeline (C -> B -> A) one item at a time until exhaustion.
    # No intermediate lists are ever created for 500,000 records.
    start_aggregation = time.perf_counter()
    total_value = sum(high_value_transactions)
    end_aggregation = time.perf_counter()

    print(f"D. Aggregation completed in: {end_aggregation - start_aggregation:.4f} seconds")
    return total_value

# --- 4. Execution and Reporting ---

if __name__ == "__main__":
    
    # Check if we are running with a smaller test size for quick debugging
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        TOTAL_RECORDS = int(sys.argv[1])

    overall_start_time = time.time()

    # Execute the processing pipeline
    result = process_large_dataset(
        num_records=TOTAL_RECORDS,
        threshold=VALUE_THRESHOLD,
        priority=TARGET_PRIORITY
    )

    overall_end_time = time.time()
    duration = overall_end_time - overall_start_time

    print("\n--- Processing Summary ---")
    print(f"Total Records Simulated: {TOTAL_RECORDS:,}")
    print(f"Target Filter: Priority='{TARGET_PRIORITY}' AND Value >= ${VALUE_THRESHOLD:,.2f}")
    print(f"Total Aggregated Value: ${result:,.2f}")
    print(f"Total Execution Time: {duration:.4f} seconds")
