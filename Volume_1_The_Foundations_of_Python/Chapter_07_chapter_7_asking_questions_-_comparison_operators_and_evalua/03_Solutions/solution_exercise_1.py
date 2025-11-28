
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

# Exercise 7.4.1 Setup
# 1. Required Credentials (Constants)
REQUIRED_USERNAME = 'admin_user'
REQUIRED_PASSWORD = 'SecurePass123!'

# 2. User Input Attempt (Variables)
input_username = 'admin_user'
input_password = 'WrongPass456'

# 3. Check Username Match
username_match = (input_username == REQUIRED_USERNAME)  # Evaluates to True

# 4. Check Password Match
password_match = (input_password == REQUIRED_PASSWORD)  # Evaluates to False

# 5. Determine Final Success
# Login is successful only if BOTH username AND password match.
login_successful = username_match and password_match

# 6. Print Result
print(f"Username Match: {username_match}")
print(f"Password Match: {password_match}")
print(f"Login Successful: {login_successful}")
