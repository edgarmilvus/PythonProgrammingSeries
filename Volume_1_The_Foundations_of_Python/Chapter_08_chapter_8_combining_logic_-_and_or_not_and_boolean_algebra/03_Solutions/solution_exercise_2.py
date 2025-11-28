
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

# Exercise 8-2: Inventory Status Flag using 'not'

# --- Product X Data ---
is_backordered_x = False
is_discontinued_x = False
quantity_in_stock_x = 30
high_demand_item_x = True

# Condition 1: Must NOT be backordered AND NOT discontinued.
# (not False) and (not False) -> True
is_available_x = not is_backordered_x and not is_discontinued_x

# Condition 2: Stock must be high OR it is high demand.
# (30 > 50 is False) or True -> True
has_sufficient_stock_x = (quantity_in_stock_x > 50) or high_demand_item_x

# Final Check: C1 AND C2 (True and True -> True)
is_ready_to_ship_x = is_available_x and has_sufficient_stock_x

print(f"Product X (Stock: {quantity_in_stock_x}, HD: {high_demand_item_x})")
print(f"Product X Status: Ready to Ship? {is_ready_to_ship_x}")

# --- Product Y Data ---
is_backordered_y = True
is_discontinued_y = False
quantity_in_stock_y = 100
high_demand_item_y = False

# Condition 1: Must NOT be backordered AND NOT discontinued.
# (not True) and (not False) -> False and True -> False
is_available_y = not is_backordered_y and not is_discontinued_y

# Condition 2: Stock must be high OR it is high demand.
# (100 > 50 is True) or False -> True
has_sufficient_stock_y = (quantity_in_stock_y > 50) or high_demand_item_y

# Final Check: C1 AND C2 (False and True -> False)
is_ready_to_ship_y = is_available_y and has_sufficient_stock_y

print(f"\nProduct Y (Stock: {quantity_in_stock_y}, HD: {high_demand_item_y})")
print(f"Product Y Status: Ready to Ship? {is_ready_to_ship_y}")
