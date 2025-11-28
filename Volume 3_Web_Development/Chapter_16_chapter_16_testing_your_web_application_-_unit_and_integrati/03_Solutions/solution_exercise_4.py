
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

# Source File: solution_exercise_4.py
# Description: Solution for Exercise 4
# ==========================================

# test_mocking.py

# Import the functions we need to test and mock
from app_setup import calculate_portfolio_value, get_current_crypto_price 

# Note: The patching path must be where the function is imported/used. 
# Since calculate_portfolio_value imports it from app_setup, that is the path.

def test_portfolio_calculation_with_mock(mocker):
    """
    Tests portfolio calculation logic by mocking the external price fetcher.
    """
    # 1. Mock Setup: Patch the external function
    mock_price_fetcher = mocker.patch(
        'app_setup.get_current_crypto_price', 
        autospec=True
    )
    
    # 2. Controlled Return Value: Define the mock's behavior
    # Configure it to return 50000.00 specifically when 'BTC' is requested
    mock_price_fetcher.return_value = 50000.00

    # Test data: 2 units of BTC
    holdings = {'BTC': 2.0}
    
    # Execute the function under test
    total_value = calculate_portfolio_value(holdings)
    
    # 3. Calculation Verification: 2.0 * 50000.00 = 100000.00
    expected_value = 100000.00
    assert total_value == expected_value
    
    # 4. Call Verification: Assert the mock was called correctly
    mock_price_fetcher.assert_called_once_with('BTC')
    
    # Ensure the real function was never executed
    # (This is implicitly handled by using autospec=True and the mock returning a value)
