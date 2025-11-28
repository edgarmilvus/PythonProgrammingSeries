
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

# Source File: basic_basic_code_example_part3.py
# Description: Basic Code Example
# ==========================================

def update_email(name, new_email):
    if name in CONTACT_DB:
        # Step 1: Retrieve the existing phone number (index 0)
        old_phone = CONTACT_DB[name][0]
        
        # Step 2: Create a brand new tuple with the old phone and new email
        new_record = (old_phone, new_email)
        
        # Step 3: Reassign the entire value to the key
        CONTACT_DB[name] = new_record
        print(f"[UPDATE] Email updated for {name} to {new_email}")
    else:
        print(f"[ERROR] Cannot update: Contact '{name}' not found.")

# Demonstration of the correct update
update_email("Alice Wonderland", "new_alice@corp.net")
display_contact("Alice Wonderland") 
