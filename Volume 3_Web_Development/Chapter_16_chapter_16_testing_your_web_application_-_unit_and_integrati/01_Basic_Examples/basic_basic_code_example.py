
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

# =======================================================
# FILE 1: pricing.py (The Application Logic)
# This file contains the function we want to verify.
# =======================================================

def calculate_discounted_price(original_price: float) -> float:
    """
    Applies a 10% discount if the price is $50.00 or higher.
    Otherwise, returns the original price unchanged.
    """
    # Define constants for clarity and easy modification
    DISCOUNT_RATE = 0.10
    MINIMUM_THRESHOLD = 50.0

    # Check the condition for applying the discount
    if original_price >= MINIMUM_THRESHOLD:
        # Step 1: Calculate the monetary value of the discount
        discount_amount = original_price * DISCOUNT_RATE
        # Step 2: Return the final price after subtraction
        return original_price - discount_amount
    else:
        # If the price is below the threshold, return it as is
        return original_price


# =======================================================
# FILE 2: test_pricing.py (The PyTest Suite)
# This file contains the tests verifying the application logic.
# PyTest automatically discovers files starting or ending with 'test_'.
# =======================================================

# 1. Import the function(s) we need to test
from pricing import calculate_discounted_price

def test_discount_applied_above_threshold():
    """Test case where the price is high enough to qualify for the discount."""
    # Arrange: Setup inputs and expected outputs
    price = 100.0
    # Expected result: 100 - (100 * 0.10) = 90.0
    expected = 90.0

    # Act: Execute the function under test
    actual = calculate_discounted_price(price)

    # Assert: Verify the actual result matches the expected result
    # PyTest captures standard 'assert' failures and provides detailed reports
    assert actual == expected, f"Failed: Expected {expected}, but got {actual}"


def test_no_discount_below_threshold():
    """Test case where the price is too low, ensuring no discount is applied."""
    # Arrange: Setup inputs
    price = 40.0
    # Expected result: 40.0 (unchanged)
    expected = 40.0

    # Act: Execute the function
    actual = calculate_discounted_price(price)

    # Assert: Verify the result
    assert actual == expected


def test_edge_case_at_threshold():
    """Test the critical boundary condition (exactly $50.00)."""
    # Arrange: Setup inputs
    price = 50.0
    # Expected result: 50 - (50 * 0.10) = 45.0
    expected = 45.0

    # Act: Execute the function
    actual = calculate_discounted_price(price)

    # Assert: Verify the result
    assert actual == expected
