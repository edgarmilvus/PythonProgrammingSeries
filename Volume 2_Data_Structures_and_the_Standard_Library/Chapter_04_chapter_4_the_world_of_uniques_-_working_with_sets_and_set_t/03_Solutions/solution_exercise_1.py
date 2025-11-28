
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

# Source File: solution_exercise_1.py
# Description: Solution for Exercise 1
# ==========================================

import random

# --- Data Setup ---
# Note: This data setup is provided in the prompt and is necessary for running the solutions.

SKU_BASE = ['P1001', 'P2050', 'P3300', 'P4112', 'P5000', 'P6789', 'P7007', 'P8080', 'P9999', 'P0001']
# Create a large list with many duplicates
raw_inventory = (SKU_BASE * 5) + ['P9999', 'P1001', 'P1234', 'P5432', 'P9000']
random.shuffle(raw_inventory)

# Critical SKUs (some present, some missing)
critical_skus = ['P1001', 'P7007', 'P5432', 'P1111', 'P0000']

# Exercise 2 Data (User IDs)
web_users = {101, 102, 103, 104, 105, 110, 111}
mobile_users = {103, 104, 106, 107, 108, 110, 112}
desktop_users = {101, 104, 109, 110, 113, 114}

# Exercise 3 Data (Caching)
PERMISSION_CACHE = {}

# Exercise 4 Data (Log Analyzer)
master_error_catalog = {'E100', 'E200', 'E300', 'E400', 'E500', 'E600', 'E700'}

# Errors found in the previous monitoring run
previous_run_errors = {'E100', 'E200', 'E300', 'E500', 'E800'} # Note E800 is unknown

# Errors found in the current monitoring run
current_run_errors = {'E100', 'E400', 'E500', 'E600', 'E900'} # Note E900 is unknown

# ---------------------------------------------------------------------

## Exercise 1: The Inventory Purge and Critical Stock Check

print("--- Exercise 1: Inventory Purge and Critical Stock Check ---")

# 1. De-duplication: Convert the list to a set to automatically enforce uniqueness.
unique_inventory_set = set(raw_inventory)
print(f"Total raw items: {len(raw_inventory)}")
print(f"Total unique items (Set size): {len(unique_inventory_set)}")

# 2. Efficiency Test (Membership)
def check_critical_status(sku_list, inventory_set):
    """
    Checks the presence of critical SKUs using the set's O(1) lookup efficiency.
    """
    print("\nChecking Critical SKU Status (O(1) Lookup):")
    for sku in sku_list:
        # Membership test using the 'in' operator on the set
        if sku in inventory_set:
            print(f"  [FOUND] SKU {sku}: In Stock.")
        else:
            print(f"  [MISSING] SKU {sku}: Critical item not found!")

# Run the check
check_critical_status(critical_skus, unique_inventory_set)

# ---------------------------------------------------------------------

## Exercise 2: Cross-Platform User Segmentation Analysis

print("\n--- Exercise 2: Cross-Platform User Segmentation Analysis ---")

# 1. Total Reach (Union: |)
# Finds all users present in any of the three sets.
total_unique_users = web_users | mobile_users | desktop_users
print(f"1. Total Unique Users (Union): {len(total_unique_users)}")
print(f"   User IDs: {sorted(list(total_unique_users))}")

# 2. Core Audience (Intersection: &)
# Finds users common to all three platforms.
core_audience = web_users & mobile_users & desktop_users
print(f"2. Core Audience (Accessed all three platforms): {core_audience}")

# 3. Mobile Exclusives (Difference: -)
# Users in Mobile, minus any user also found in Web or Desktop.
web_or_desktop = web_users | desktop_users
mobile_exclusives = mobile_users - web_or_desktop
print(f"3. Mobile Exclusive Users: {mobile_exclusives}")

# 4. Platform Switchers (Symmetric Difference: ^)
# Users who used Web OR Mobile, but NOT both (exclusive OR).
web_mobile_switchers = web_users ^ mobile_users
print(f"4. Web/Mobile Switchers (Symmetric Difference): {web_mobile_switchers}")

# ---------------------------------------------------------------------

## Exercise 3: Immutable Configuration Caching using `frozenset`

print("\n--- Exercise 3: Immutable Configuration Caching using frozenset ---")

def get_permission_status(required_permissions):
    """
    Uses frozenset as a hashable, immutable dictionary key for caching.
    """
    # 1. Convert the input list to a frozenset. This ensures the key is hashable 
    # and that order (e.g., ['A', 'B'] vs ['B', 'A']) is irrelevant.
    permission_key = frozenset(required_permissions)

    # 2. Check Cache
    if permission_key in PERMISSION_CACHE:
        print(f"  [CACHE HIT] Retrieving status for {sorted(required_permissions)}...")
        return PERMISSION_CACHE[permission_key]

    # 3. Simulate Expensive Calculation (Cache Miss)
    print(f"  [CACHE MISS] Performing expensive database lookup for {sorted(required_permissions)}...")
    
    # Mock calculation logic: Access is granted if 'READ' is required.
    if 'READ' in permission_key:
        result = "Access Granted: READ permission confirmed."
    else:
        result = "Access Denied: Insufficient permissions."
    
    # 4. Store result in cache using the frozenset key
    PERMISSION_CACHE[permission_key] = result
    return result

# Test 1: Initial call (Cache Miss)
status_a = get_permission_status(['WRITE', 'READ', 'AUDIT'])
print(f"Result A: {status_a}")

# Test 2: Same permissions, different order (Cache Hit expected)
status_b = get_permission_status(['AUDIT', 'READ', 'WRITE'])
print(f"Result B: {status_b}")

# Test 3: Different set of permissions (Cache Miss expected)
status_c = get_permission_status(['EXECUTE'])
print(f"Result C: {status_c}")

# ---------------------------------------------------------------------

## Exercise 4: Interactive Challenge: Extending the Log Analyzer

print("\n--- Exercise 4: Log Analyzer Extension (Set Comparison) ---")

# 1. Resolved Errors (Set Difference: Previous - Current)
# Errors that were present before but are now gone.
resolved_errors = previous_run_errors - current_run_errors
print(f"1. Resolved/Transient Errors (Previous - Current): {resolved_errors}")

# 2. New Errors (Set Difference: Current - Previous)
# Errors that appeared in the current run but not the previous one.
new_errors = current_run_errors.difference(previous_run_errors)
print(f"2. Newly Introduced Errors (Current - Previous): {new_errors}")

# 3. Integrity Check (Subset Testing)
# Verify if the current errors are all documented in the master catalog.
is_catalog_complete = current_run_errors.issubset(master_error_catalog)

if is_catalog_complete:
    print("\n3. Integrity Check: PASSED. All current errors are recognized in the master catalog.")
else:
    # If the check fails, calculate which specific errors are unknown.
    unknown_errors = current_run_errors - master_error_catalog
    print("\n3. Integrity Check: FAILED.")
    print(f"    Alert: The following errors are UNKNOWN and not in the master catalog: {unknown_errors}")
