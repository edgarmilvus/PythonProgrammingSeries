
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

# Exercise 8-3: Tiered Pricing and Discount Logic

# Customer Z Test Data
is_premium_member = False
purchase_quantity = 15
total_cost = 450.00
is_holiday_sale = True
DISCOUNT_RATE = 0.20 # 20%

# Major Condition A: Volume Discount
# (purchase_quantity > 10 AND total_cost > 500)
# (True AND False) -> False
condition_A = (purchase_quantity > 10) and (total_cost > 500.00)

# Major Condition B: Member/Sale Discount
# ((is_premium_member OR is_holiday_sale) AND total_cost > 100)
# ((False OR True) AND True) -> True
condition_B = (is_premium_member or is_holiday_sale) and (total_cost > 100.00)

# Final Logic: A OR B (False OR True) -> True
applies_discount = condition_A or condition_B

print(f"Initial Cost: ${total_cost:.2f}")
print(f"Applies Discount (20%): {applies_discount}")

if applies_discount:
    discount_amount = total_cost * DISCOUNT_RATE
    final_cost = total_cost - discount_amount
    print(f"Discount Applied: ${discount_amount:.2f}")
    print(f"Final Cost: ${final_cost:.2f}")
else:
    print("No discount applied.")
    print(f"Final Cost: ${total_cost:.2f}")
