
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

# Constants used throughout the script for configuration and formatting
MAX_ITEMS = 5
CURRENCY_SYMBOL = "USD"

# 1. Safe Integer Input Function
# This function handles getting input specifically for whole numbers (quantities).
def get_int_input(prompt):
    # Loop indefinitely until valid integer input is received
    while True:
        raw_input = input(prompt).strip()
        
        # Attempt explicit type conversion using int(). This is where errors usually occur.
        try:
            converted_value = int(raw_input)
            
            # Additional validation: Quantity must be non-negative
            if converted_value < 0:
                print("Error: Quantity must be non-negative. Please try again.")
                # Continue skips the rest of the loop body and starts the next iteration
                continue
            
            # If conversion and validation succeed, return the numerical result
            return converted_value
            
        # Catch the ValueError specifically if conversion fails (e.g., input is "ten" or "10.5")
        except ValueError:
            print(f"Input Error: '{raw_input}' cannot be converted to an integer (whole number).")
            print("Please enter a valid whole number.")

# 2. Safe Float Input Function
# This function handles getting input specifically for decimal numbers (prices).
def get_float_input(prompt):
    # Loop indefinitely until valid float input is received
    while True:
        raw_input = input(prompt).strip()
        
        # Attempt explicit type conversion using float()
        try:
            converted_value = float(raw_input)
            
            # Additional validation: Price must be non-negative
            if converted_value < 0:
                print("Error: Price must be non-negative. Please try again.")
                continue
                
            # If conversion and validation succeed, return the numerical result
            return converted_value
            
        # Catch the ValueError if conversion fails (e.g., input is "free")
        except ValueError:
            print(f"Input Error: '{raw_input}' cannot be converted to a decimal number.")
            print("Please enter a valid numerical price (e.g., 19.99).")

# 3. Processing Logic for a Single Item
def process_item_input(item_number):
    print(f"\n--- Entering Item {item_number} Details ---")

    # Item Name remains a string
    item_name = input("Enter Item Name: ").strip()
    if not item_name:
        item_name = f"Unnamed Item {item_number}"

    # Get Quantity (delegates to safe int conversion)
    quantity = get_int_input("Enter Quantity in Stock: ")

    # Get Unit Price (delegates to safe float conversion)
    unit_price = get_float_input("Enter Unit Price: ")

    # Calculate the item's total value
    # NOTE: This uses IMPLICIT type conversion. Python automatically promotes the int (quantity)
    # to a float before multiplying it by unit_price (float) to maintain precision.
    item_total_value = quantity * unit_price

    # Return the collected and calculated data as a dictionary
    return {
        "name": item_name,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_value": item_total_value
    }

# 4. Report Generation
def generate_report(inventory_list):
    if not inventory_list:
        print("\nInventory calculation complete. No items were processed.")
        return

    grand_total = 0.0
    print("\n" + "="*70)
    print("INVENTORY VALUATION REPORT".center(70))
    print("="*70)

    # Print header
    print(f"{'Item Name':<30} | {'Qty':>8} | {'Unit Price':>15} | {'Total Value':>15}")
    print("-" * 70)

    # Iterate through processed items
    for item in inventory_list:
        # Accumulate grand total
        grand_total += item['total_value']

        # Explicitly converting numerical values back to strings for formatted printing
        # We use f-strings to format the floats to two decimal places, effectively casting to a formatted string
        qty_str = str(item['quantity'])
        price_str = f"{item['unit_price']:.2f}"
        total_str = f"{item['total_value']:.2f}"

        print(
            f"{item['name']:<30} | "
            f"{qty_str:>8} | "
            f"{CURRENCY_SYMBOL} {price_str:>11} | "
            f"{CURRENCY_SYMBOL} {total_str:>11}"
        )

    print("-" * 70)

    # Final display of the grand total
    grand_total_str = f"{grand_total:.2f}"
    print(f"GRAND TOTAL INVENTORY VALUE:".ljust(40) + f"{CURRENCY_SYMBOL} {grand_total_str:>25}")
    print("="*70)


# 5. Main Execution Block
def main():
    print("--- Stock Valuation System Initialized ---")
    print(f"You can process up to {MAX_ITEMS} items. Enter 'done' when prompted to finish early.")

    inventory_data = []
    item_count = 0

    # Main loop to collect data
    while item_count < MAX_ITEMS:
        item_count += 1

        # Check for early exit condition after the first item
        if item_count > 1:
            continue_input = input("\nPress Enter to add another item, or type 'done' to calculate report: ").strip().lower()
            if continue_input == 'done':
                break

        # Process the item input, handling all conversions and validation
        item_details = process_item_input(item_count)

        # Append the successfully processed dictionary to the list
        if item_details:
            inventory_data.append(item_details)

        # If max items reached, break the loop
        if item_count >= MAX_ITEMS:
            print("\nMaximum item limit reached.")
            break

    # Generate the final report
    generate_report(inventory_data)


# Standard Python entry point
if __name__ == "__main__":
    main()
