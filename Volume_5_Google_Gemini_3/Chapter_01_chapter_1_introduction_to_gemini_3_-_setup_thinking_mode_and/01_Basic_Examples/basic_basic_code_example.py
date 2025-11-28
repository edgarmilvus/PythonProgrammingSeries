
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

import os
from google import genai
from google.genai import types

# --- Configuration ---
MODEL_ID = "gemini-3-pro-preview"

# 1. Define the complex, reasoning-heavy prompt
# This C++ snippet contains a classic race condition.
COMPLEX_CODE_SNIPPET = """
#include <iostream>
#include <thread>
#include <mutex>

int shared_data = 0;
std::mutex mtx;

void increment_data() {
    for (int i = 0; i < 10000; ++i) {
        // Line 11: The critical section where the race occurs
        shared_data++; 
    }
}

int main() {
    std::thread t1(increment_data);
    std::thread t2(increment_data);

    t1.join();
    t2.join();

    std::cout << "Final shared data: " << shared_data << std::endl;
    return 0;
}
"""

PROMPT = (
    "Analyze the following C++ multi-threaded snippet. "
    "Identify the specific line number where the race condition occurs "
    "and explain why it leads to unpredictable results. "
    "Snippet:\n\n" + COMPLEX_CODE_SNIPPET
)

# 2. Client Initialization (EAFP Style)
# The client automatically loads the API key from the GEMINI_API_KEY environment variable.
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing client: {e}")
    print("FATAL: Please ensure your GEMINI_API_KEY environment variable is set.")
    # Exit gracefully if the key isn't found
    exit()

# 3. Execute the generation request
# By omitting the 'config' parameter, we default to Gemini 3 Pro's 'high' thinking level.
print(f"--- Sending Request to {MODEL_ID} (Default High Thinking) ---")
response = client.models.generate_content(
    model=MODEL_ID,
    contents=PROMPT,
)

# 4. Display the result
print("\n--- Gemini 3 Pro Analysis Result ---")
print(response.text)

print("\n--- Request Metadata ---")
print(f"Model ID used: {response.model}")
print(f"Response status: {response.candidates[0].finish_reason.name}")
