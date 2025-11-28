
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

# test_models.py

from app_setup import User

def test_valid_user_data():
    """Tests a successful validation case."""
    valid_data = {
        'username': 'testuser',
        'email': 'test.user@example.com',
        'password': 'StrongPassword123'  # Length > 8
    }
    assert User.validate_user_data(valid_data) is True

def test_password_too_short():
    """Tests failure when the password is less than the minimum length (8)."""
    short_password_data = {
        'username': 'testuser',
        'email': 'test.user@example.com',
        'password': 'short'  # Length 5
    }
    assert User.validate_user_data(short_password_data) is False

def test_invalid_email_format():
    """Tests failure when the email format is incorrect."""
    invalid_email_data = {
        'username': 'testuser',
        'email': 'user@domain',  # Missing TLD (e.g., .com)
        'password': 'StrongPassword123'
    }
    assert User.validate_user_data(invalid_email_data) is False

def test_missing_required_field():
    """Tests failure when a critical field (username) is missing."""
    missing_field_data = {
        'email': 'test.user@example.com',
        'password': 'StrongPassword123'
    }
    # The validation function should gracefully return False if fields are missing
    assert User.validate_user_data(missing_field_data) is False
