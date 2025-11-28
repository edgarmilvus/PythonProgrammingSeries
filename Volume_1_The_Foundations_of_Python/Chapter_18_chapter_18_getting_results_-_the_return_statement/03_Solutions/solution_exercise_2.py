
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

def analyze_purchase(base_price, tax_rate):
    """
    Calculates the total cost and the tax amount for a purchase.
    Returns both values as a tuple (total_cost, tax_amount).
    """
    # Calculate the tax amount based on the rate
    tax_amount = base_price * tax_rate
    
    # Calculate the total cost
    total_cost = base_price + tax_amount
    
    # Returning multiple values packaged as a tuple.
    return total_cost, tax_amount  # Parentheses are optional for tuple return

# Test Case
price = 150.00
rate = 0.065 # 6.5% tax rate

# Tuple unpacking: the two elements of the returned tuple are assigned 
# simultaneously to final_price and tax_paid.
final_price, tax_paid = analyze_purchase(price, rate)

print(f"Original Price: ${price:.2f}")
print(f"Tax Rate: {rate * 100:.1f}%")
print(f"---")
print(f"Total Cost: ${final_price:.2f}")
print(f"Tax Paid: ${tax_paid:.2f}")
