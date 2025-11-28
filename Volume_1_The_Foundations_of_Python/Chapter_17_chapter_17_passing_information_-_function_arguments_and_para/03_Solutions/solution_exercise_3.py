
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

def generate_greeting(recipient, phrase="Hello, welcome to the system"):
    """
    Generates a customized greeting message.

    Args:
        recipient (str): The name of the person receiving the greeting (required).
        phrase (str, optional): The introductory phrase. 
                                Defaults to "Hello, welcome to the system".

    Returns:
        str: The complete formatted greeting.
    """
    # Construct the final string, adding consistent punctuation.
    return f"{phrase}, {recipient}!"

# 3. Standard Greeting (Uses default phrase)
name_1 = "Dr. Evelyn Reed"
greeting_standard = generate_greeting(name_1)
print(f"1. Standard Greeting: {greeting_standard}")

# 4. Custom Greeting (Positional Override)
# The custom phrase is passed as the second positional argument.
name_2 = "Mr. John Smith"
phrase_custom_pos = "Good morning, esteemed colleague"
greeting_custom_pos = generate_greeting(name_2, phrase_custom_pos)
print(f"2. Custom Positional Greeting: {greeting_custom_pos}")

# 5. Custom Greeting (Keyword Override)
# The phrase is set using its keyword name for clarity.
name_3 = "Agent 007"
phrase_custom_kw = "Attention required"
greeting_custom_kw = generate_greeting(name_3, phrase=phrase_custom_kw)
print(f"3. Custom Keyword Greeting: {greeting_custom_kw}")
