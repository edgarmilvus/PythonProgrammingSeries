
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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

# 1. Initialization
order_total = 250.00
customer_status = "Standard"  # Test cases: "Premium", "Standard", "New"
discount_rate = 0.0

# Define test values for clarity
# order_total = 150.00
# customer_status = "New"

# 2. Complex Conditionals: Apply rules in priority order (15%, 10%, 5%, 0%)

# Rule 1: Premium Customer Tier (Highest priority, 15% flat)
if customer_status == "Premium":
    discount_rate = 0.15
    reason = "Premium Member Discount"

# Rule 2: Bulk Order Discount (10% for non-Premium orders >= $200)
elif customer_status != "Premium" and order_total >= 200.00:
    discount_rate = 0.10
    reason = "Bulk Order Discount"

# Rule 3: First-Time Buyer Incentive (5% for New customers >= $50, if not already discounted)
elif customer_status == "New" and order_total >= 50.00:
    discount_rate = 0.05
    reason = "First-Time Buyer Incentive"

# Rule 4: No Discount
else:
    discount_rate = 0.0
    reason = "No applicable discount"

# 3. Calculation
final_price = order_total * (1.0 - discount_rate)
discount_percentage = discount_rate * 100

# 4. Output
print(f"--- E-Commerce Discount Engine ---")
print(f"Order Total: ${order_total:.2f}")
print(f"Customer Status: {customer_status}")
print(f"Applied Discount: {discount_percentage:.0f}% ({reason})")
print(f"Final Price: ${final_price:.2f}")
