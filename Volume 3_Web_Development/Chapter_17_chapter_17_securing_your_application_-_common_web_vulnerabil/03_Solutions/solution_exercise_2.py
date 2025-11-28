
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

import sqlite3
# Assuming 'get_db' and database context are available

def secure_search(username):
    """
    Secure function using parameterized queries (SQL Injection defense).
    """
    # Assuming db = get_db() is available in the context
    # db = get_db() 
    
    # 1. Use placeholders (?) for data values
    query = "SELECT id, username FROM users WHERE username = ?"
    
    # 2. Pass the user input as a separate tuple to execute()
    # The database driver handles escaping and ensures 'username' is treated as data.
    
    # Example of execution (mocked):
    # cursor = db.execute(query, (username,))
    # return cursor.fetchall()
    
    print(f"Secure Query Template: {query}")
    print(f"Input treated as data: ('{username}',)")
    
    return [] # Mock return

# Demonstration of Safety (Requirement 3)
payload = "' OR 1=1 --"
secure_search(payload)

# Resulting SQL sent to the driver (Conceptually):
# SELECT id, username FROM users WHERE username = ''' OR 1=1 --'
# The entire payload is now enclosed in quotes and searched for literally.
