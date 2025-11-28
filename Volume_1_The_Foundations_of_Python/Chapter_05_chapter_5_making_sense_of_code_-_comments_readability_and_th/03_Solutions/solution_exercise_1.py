
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

# Source File: solution_exercise_1.py
# Description: Solution for Exercise 1
# ==========================================

"""
financial_utility.py

Module Purpose:
Provides core financial calculation utilities, specifically focusing on
compound interest calculations for investment forecasting. This module is
intended to be a reliable source for standard financial formulas.
"""

import math

def calculate_future_value(principal: float, rate: float, years: int) -> float:
    """
    Calculates the future value of an investment compounded annually.

    The calculation uses the standard compound interest formula:
    FV = P * (1 + r)^t
    Where:
        FV = Future Value
        P = Principal amount
        r = Annual interest rate (as a decimal)
        t = Number of years

    Parameters
    ----------
    principal : float
        The initial amount of money invested (P). Must be positive.
    rate : float
        The annual interest rate, expressed as a percentage (e.g., 5 for 5%).
    years : int
        The number of years the money is invested for (t). Must be non-negative.

    Returns
    -------
    float
        The calculated future value of the investment.
    """
    
    # Convert the rate percentage (e.g., 5) into a decimal (0.05).
    # This conversion is necessary because the financial formula requires 
    # the rate 'r' to be expressed as a decimal fraction.
    decimal_rate = rate / 100.0
    
    # Calculate the growth factor: (1 + r)^t
    # This represents the total multiplicative growth over the investment period.
    growth_factor = math.pow((1.0 + decimal_rate), years)
    
    # Apply the growth factor to the initial principal (P) to get the final value (FV).
    future_value = principal * growth_factor
    
    return future_value

# Example Usage:
# future_val = calculate_future_value(principal=1000, rate=5, years=10)
# print(f"Future Value: {future_val:.2f}") 
