
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
# ----------------------------------------------------------------------
def calculate_rectangle_area(width, height):
    """
    Calculates the area of a rectangle.

    This function takes two numerical inputs (width and height)
    and returns their product, representing the area.
    """
    # 1. The function body starts here (indicated by indentation)
    
    # Perform the core calculation: multiplication
    area = width * height
    
    # 2. Return the calculated value back to the caller
    return area

# Main Execution Block
# ----------------------------------------------------------------------

# Define the dimensions of the first room (Arguments)
living_room_width = 7.5
living_room_height = 10.0

# Call the function, passing the arguments, and store the returned result
# The function executes, calculates 7.5 * 10.0, and returns 75.0
living_room_area = calculate_rectangle_area(living_room_width, living_room_height)

# Define the dimensions of a second area
kitchen_width = 4.0
kitchen_height = 6.0

# Call the function again with different inputs
kitchen_area = calculate_rectangle_area(kitchen_width, kitchen_height)

# Output the results
print("--- Floor Area Calculations ---")
print(f"Living Room: {living_room_width}m x {living_room_height}m")
print(f"Area needed: {living_room_area} sq meters.")
print("-" * 30)
print(f"Kitchen: {kitchen_width}m x {kitchen_height}m")
print(f"Area needed: {kitchen_area} sq meters.")
