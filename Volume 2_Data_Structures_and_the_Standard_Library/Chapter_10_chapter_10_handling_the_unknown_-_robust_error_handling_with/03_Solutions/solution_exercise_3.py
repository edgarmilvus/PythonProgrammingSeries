
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

class InsufficientFundsError(Exception):
    """
    Custom exception raised when a withdrawal would drop the account balance
    below the required minimum threshold.
    """
    def __init__(self, current_balance, amount_to_withdraw, required_min=100):
        self.current_balance = current_balance
        self.amount_to_withdraw = amount_to_withdraw
        self.required_min = required_min
        self.resulting_balance = current_balance - amount_to_withdraw

        # Define a detailed message for when the exception is printed
        super().__init__(f"Withdrawal failed: Account balance ({self.current_balance:.2f}) "
                         f"would drop to {self.resulting_balance:.2f}, "
                         f"which is below the required minimum of ${self.required_min:.2f}.")

def make_withdrawal(current_balance, amount_to_withdraw, min_balance=100):
    """
    Attempts a withdrawal, raising InsufficientFundsError if the minimum balance is violated.
    """
    new_balance = current_balance - amount_to_withdraw

    if new_balance < min_balance:
        # Raise the custom exception, passing relevant data for the error message
        raise InsufficientFundsError(current_balance, amount_to_withdraw, min_balance)

    # If successful, return the new balance
    return new_balance

# Demonstration Block (Required for testing the custom exception)
def run_bank_simulation():
    initial_balance = 500.00
    withdrawal_amount = 450.00 # This withdrawal will fail (50 < 100 min)

    print(f"Starting balance: ${initial_balance:.2f}")

    try:
        final_balance = make_withdrawal(initial_balance, withdrawal_amount)
        print(f"Successful withdrawal of ${withdrawal_amount:.2f}.")
        print(f"New balance: ${final_balance:.2f}")

    except InsufficientFundsError as e:
        # Catch the specific custom error
        print("\n--- TRANSACTION ALERT ---")
        # Printing 'e' uses the custom message defined in the exception's __init__
        print(f"SYSTEM ERROR: {e}")
        print(f"Action required: Advise customer to adjust withdrawal amount.")
        print("-------------------------")

# run_bank_simulation()
