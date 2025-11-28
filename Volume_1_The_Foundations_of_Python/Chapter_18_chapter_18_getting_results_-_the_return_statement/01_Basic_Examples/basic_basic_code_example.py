
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

# Function Definition Block
# 1. Define a function that accepts two numerical inputs (parameters)
def calculate_rectangle_area(length, width):
    """
    Calculates the area of a rectangle.
    The result (area) is explicitly returned to the caller.
    """
    
    # 2. Perform the calculation and store the intermediate result locally
    # This variable 'area' only exists inside this function
    area = length * width
    
    # 3. The 'return' statement immediately exits the function and passes the 
    # value stored in 'area' back to the point where the function was called.
    return area 

# --- Execution Block (The main script flow) ---

# 4. Define the input dimensions for the first use case (a desk)
desk_length = 150  # Length in centimeters
desk_width = 80    # Width in centimeters

# 5. Call the function. The function executes, returns a value (12000), 
# and that value replaces the function call expression.
desk_area = calculate_rectangle_area(desk_length, desk_width)

# 6. Print the final result, demonstrating that the returned value was successfully 
# captured and stored in the 'desk_area' variable.
print(f"The desk area is: {desk_area} square cm.")

# 7. Demonstrate reusability: Calculate the area of a room
room_length = 400
room_width = 300
    
# 8. Call the function again. The returned result is stored in a new variable.
room_area_result = calculate_rectangle_area(room_length, room_width)
    
print(f"The room area is: {room_area_result} square cm.")
