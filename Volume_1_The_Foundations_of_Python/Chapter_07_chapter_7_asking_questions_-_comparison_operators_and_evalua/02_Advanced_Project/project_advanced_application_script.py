
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

# --- Configuration Constants ---
# These constants define the numerical thresholds used for comparisons.
LOW_STOCK_THRESHOLD = 20
URGENT_THRESHOLD = 5
# Note: For simplicity in this foundational chapter, dates are represented as YYYYMMDD integers,
# allowing us to use standard comparison operators (<, >) effectively.

# Simulate today's date for comparison purposes (2024 September 15)
TODAY_DATE = 20240915

# Sample Inventory Data (List of Dictionaries)
inventory = [
    {"name": "Widget A", "quantity": 15, "price": 10.50, "expiration_date": 20241020},
    {"name": "Gadget B", "quantity": 4, "price": 45.00, "expiration_date": 20240914}, # Expired & Urgent
    {"name": "Tool C", "quantity": 55, "price": 12.00, "expiration_date": 20250101},
    {"name": "Part D", "quantity": 21, "price": 3.99, "expiration_date": 20240920}, # Near expiry
    {"name": "Unit E", "quantity": 1, "price": 99.99, "expiration_date": 20240915}, # Critical, expiring today
    {"name": "Supply F", "quantity": 18, "price": 5.00, "expiration_date": 20241231}, # Low stock
    {"name": "Material G", "quantity": 6, "price": 2.50, "expiration_date": 20250301}, # Urgent stock
]

def get_stock_status(quantity):
    """
    Evaluates the quantity against defined thresholds using comparison operators.
    Returns a string indicating the stock level status.
    """
    # Comparison 1: Is the quantity less than or equal to the urgent threshold?
    # This comparison produces a Boolean (True/False) that dictates the block execution.
    if quantity <= URGENT_THRESHOLD:
        return "CRITICAL REORDER"
        
    # Comparison 2: If not critical, is it less than or equal to the low stock threshold?
    # Note: Because of the 'elif', we already know quantity > URGENT_THRESHOLD.
    elif quantity <= LOW_STOCK_THRESHOLD:
        return "LOW STOCK WARNING"
        
    # If neither comparison was True, the stock is adequate.
    else:
        return "ADEQUATE"

def check_expiration_status(exp_date, today_date):
    """
    Compares the item's expiration date against today's date.
    Returns a string indicating the expiration status.
    """
    # Comparison 3: Check for absolute expiration (Is the expiration date numerically smaller than today?)
    if exp_date < today_date:
        return "EXPIRED"

    # Comparison 4: Check for immediate expiration (Is the expiration date exactly today?)
    elif exp_date == today_date:
        return "EXPIRES TODAY"

    # Comparison 5: Check for near expiration (Within 5 days, simplified using integer subtraction)
    # We are asking: Is the difference between the two dates less than or equal to 5?
    elif (exp_date - today_date) <= 5:
         return "NEAR EXPIRY (5 days)"

    # If all previous comparisons were False, the item is safe.
    else:
        return "OK"

# --- Main Reporting Logic ---

print("--- Inventory Management Status Report (Date: {}) ---".format(TODAY_DATE))
print("-" * 75)

# Initialize counters using comparison results
total_urgent_items = 0
total_expired_items = 0
total_low_items = 0

for item in inventory:
    name = item["name"]
    qty = item["quantity"]
    exp = item["expiration_date"]
    action_required = False # Default assumption: No action needed (LBYL approach)

    # Determine stock status using comparison functions
    stock_status = get_stock_status(qty)
    exp_status = check_expiration_status(exp, TODAY_DATE)

    # Comparison 6: Check if stock status requires urgent action (Equality check)
    if stock_status == "CRITICAL REORDER":
        total_urgent_items += 1
        action_required = True
        
    # Comparison 7: Check if stock status requires warning (Equality check)
    elif stock_status == "LOW STOCK WARNING":
        total_low_items += 1
        # Low stock is a warning, not immediate action unless combined with expiry.

    # Comparison 8: Check if item is expired or expiring today (Equality check and logical OR)
    if exp_status == "EXPIRED" or exp_status == "EXPIRES TODAY":
        total_expired_items += 1
        # Comparison 9: If expired, action is definitely required
        action_required = True
        
    # Comparison 10: Check if item is near expiry AND low stock (Logical AND)
    elif exp_status == "NEAR EXPIRY (5 days)" and stock_status == "LOW STOCK WARNING":
        action_required = True # Elevate status if both conditions are True

    # Comparison 11: Determine final output format based on action requirement (Boolean comparison)
    if action_required == True:
        # Use f-string formatting to display results based on comparisons
        report_line = f"[!!! ACTION REQUIRED !!!] {name:<12} (Qty: {qty:2}) | Stock: {stock_status:<20} | Expiration: {exp_status}"
    else:
        report_line = f"[--- OK ---] {name:<12} (Qty: {qty:2}) | Stock: {stock_status:<20} | Expiration: {exp_status}"

    print(report_line)

print("-" * 75)
print("\n--- Summary Statistics ---")

# Comparison 12: Check if any urgent items exist (Greater than zero check)
if total_urgent_items > 0:
    print(f"Status RED: {total_urgent_items} items require CRITICAL REORDER.")
else:
    print("No critical stock issues detected.")
    
# Comparison 13: Check if any expired items exist (Inequality check)
if total_expired_items != 0:
    print(f"Status RED: {total_expired_items} items are expired or expiring today.")

# Comparison 14: Check if any low stock items exist (Greater than zero check)
if total_low_items > 0:
    print(f"Status YELLOW: {total_low_items} items are at LOW STOCK WARNING level.")

# Comparison 15: Final check for overall operational status (Multiple equality checks combined with AND)
if total_urgent_items == 0 and total_expired_items == 0 and total_low_items == 0:
    print("\nSystem Status: GREEN (Nominal operations). All stock levels are adequate.")
else:
    print("\nSystem Status: ATTENTION REQUIRED (Review RED and YELLOW items).")
