
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

# Source File: basic_basic_code_example.py
# Description: Basic Code Example
# ==========================================

# Stock Price Tracker Example: Demonstrating Advanced Slicing

# 1. Define the initial data structure (A list of daily closing prices)
stock_prices = [101.5, 102.1, 100.9, 103.5, 104.0, 105.2, 106.8, 107.1, 108.3, 109.5]
# Note: This list has 10 elements. Positive indices run from 0 to 9.
# Negative indices run from -10 (first element) to -1 (last element).

print("--- Original Data and Context ---")
print(f"Prices: {stock_prices}")
print(f"Length of Data: {len(stock_prices)}")
print("-" * 25)

# 2. Basic Slicing: Accessing the first five days (Indices 0 up to 5, excluding 5)
# Syntax: [start:stop]
first_half = stock_prices[0:5]
print(f"1. First 5 days (0:5): {first_half}")

# 3. Negative Indexing: Accessing the last three days
# When the 'start' index is negative, Python counts backward from the end.
# Leaving the 'stop' index blank means going all the way to the end of the sequence.
last_three_days = stock_prices[-3:]
print(f"2. Last 3 days (-3:): {last_three_days}")

# 4. Step Slicing: Getting prices from every other day (Step = 2)
# Syntax: [start:stop:step]. Leaving start/stop blank uses the sequence boundaries.
every_other_day = stock_prices[::2]
print(f"3. Prices on every other day (::2): {every_other_day}")

# 5. Combining Negative Indices and Steps: Getting the last 5 days, but only every other one
# Start at index -5 (the 6th element), go to the end, step by 2
recent_filtered = stock_prices[-5::2]
print(f"4. Filtered recent 5 days (-5::2): {recent_filtered}")

# 6. Reversing the List: The ultimate step trick
# A step of -1 means traversing the sequence backward, from end to start.
reversed_prices = stock_prices[::-1]
print(f"5. Prices in reverse order (::-1): {reversed_prices}")
