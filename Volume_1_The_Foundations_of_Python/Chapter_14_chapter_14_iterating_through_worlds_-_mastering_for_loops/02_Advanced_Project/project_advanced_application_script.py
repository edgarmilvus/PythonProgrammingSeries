
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

# ----------------------------------------------------------------------
# SCRIPT: Product Catalog Validator and Summarizer
# Objective: Process product data, enforce integrity rules, and calculate value.
# Demonstrates: for loops, enumerate, tuple unpacking, range(), break, continue.
# ----------------------------------------------------------------------

# 1. Configuration and Constants
MAX_CRITICAL_ERRORS = 3       # Threshold for halting processing
MIN_PRICE_THRESHOLD = 0.01    # Minimum acceptable price for a product
CATALOG_VERSION = "2024.Q3"   # Metadata for reporting

# Simulated Product Data: (ID, Name, Price, Stock_Level)
# Note the intentional inclusion of errors (None ID, 0.00 price, negative price)
product_catalog = [
    (1001, "Laptop Pro X", 1299.99, 50),
    (1002, "Mouse Ergonomic", 25.50, 150),
    (1003, "Keyboard Mechanical", 99.00, 0),
    (1004, "Monitor 4K Ultra", 0.00, 30),      # Minor Error: Price is zero
    (None, "Cable HDMI 2.1", 15.00, 200),     # Critical Error 1: Missing ID
    (1006, "Webcam HD", 55.99, 75),
    (1007, "Software License", -10.00, 100),  # Minor Error: Negative price
    (1008, "USB Drive 128GB", 19.99, 300),
    (1009, "Headset Gaming", 75.00, 10),
    (None, "Power Supply Unit", 80.00, 50),    # Critical Error 2: Missing ID
    (1011, "External SSD 1TB", 150.00, 40),
    (None, "Docking Station", 200.00, 15)     # Critical Error 3: Missing ID (Will trigger break)
]

# 2. Initialization of Tracking Variables
valid_product_count = 0
invalid_product_count = 0
critical_error_count = 0
total_inventory_value = 0.0

print(f"--- Starting Catalog Validation (Version: {CATALOG_VERSION}) ---")
print(f"Max allowable critical errors: {MAX_CRITICAL_ERRORS}\n")

# 3. Main Processing Loop
# Use enumerate to get both the index (for reporting) and the item (product tuple)
for index, product in enumerate(product_catalog):
    # Unpack the tuple for readable access to product attributes
    product_id, name, price, stock = product

    # Display current iteration status
    print(f"[{index + 1}/{len(product_catalog)}] Processing Product: {name}...")

    # A. CRITICAL ERROR CHECK (Missing ID)
    # If the primary key (ID) is missing, this is a severe data integrity issue.
    if product_id is None:
        critical_error_count += 1
        print(f"  [ERROR] Critical: Product '{name}' has no defined ID.")

        # Check if the cumulative error count meets the predefined threshold.
        if critical_error_count >= MAX_CRITICAL_ERRORS:
            print("\n!!! CRITICAL THRESHOLD REACHED. HALTING CATALOG PROCESSING. !!!")
            break # Exit the main 'for' loop immediately, ignoring remaining items
        
        # If the threshold is not reached, skip calculation for this item and move to the next.
        continue # Skip the rest of the loop block for this iteration

    # B. MINOR VALIDATION CHECK (Price Integrity)
    # If the price is invalid (zero or negative), we mark it as invalid and skip processing.
    if price <= MIN_PRICE_THRESHOLD:
        invalid_product_count += 1
        print(f"  [WARNING] Skipping: Price (${price:.2f}) is invalid or zero.")
        continue # Skip the calculation phase and proceed to the next product

    # C. SUCCESSFUL PROCESSING
    # This block is only reached if both critical and minor checks pass
    valid_product_count += 1
    
    # Calculate the total value of the stock for this item
    item_value = price * stock
    total_inventory_value += item_value

    print(f"  [OK] Validated. Value: ${item_value:,.2f}")

# 4. Post-Processing and Summary Generation
print("\n--- Validation Complete ---")

# Use a secondary 'for' loop with range() to generate a formatted separator line
separator = ""
for i in range(40):
    separator += "="
print(separator)

# Check if the loop completed naturally or was broken prematurely
products_checked = index + 1 if 'index' in locals() else 0

print(f"Total Products Submitted: {len(product_catalog)}")
print(f"Total Products Checked: {products_checked}")
print(f"Total Valid Products Processed: {valid_product_count}")
print(f"Total Invalid (Price Issues) Products: {invalid_product_count}")
print(f"Total Critical Errors Encountered: {critical_error_count}")
print(f"Total Estimated Inventory Value (Valid Items Only): ${total_inventory_value:,.2f}")
print(separator)

# 5. Final Status Reporting
if critical_error_count >= MAX_CRITICAL_ERRORS:
    print("STATUS: FAILED (Processing halted prematurely due to critical integrity breach).")
elif valid_product_count == 0 and len(product_catalog) > 0:
    print("STATUS: WARNING (All products failed validation checks).")
else:
    print("STATUS: SUCCESS (Catalog processed successfully).")
