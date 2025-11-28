
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

# Source File: theory_theoretical_foundations_part6.py
# Description: Theoretical Foundations
# ==========================================

# Initialize router with empirically determined threshold
router = CapabilityAwareRouter(capability_threshold=65)

# Test Case 1: Simple query (should use Flash)
simple_query = "What is the capital of France?"
result1 = router.execute_request(simple_query, user_tier="standard")

# Test Case 2: Complex query (should upgrade to Pro)
complex_query = """
Analyze the following merger agreement for potential conflicts:
Section 4.2 states that all intellectual property transfers to Acquirer upon closing.
Section 9.7 states that Target retains all IP rights for pre-existing technology.
Section 12.1 defines 'pre-existing technology' as any IP developed before January 1, 2023.
Section 4.2 was executed on December 15, 2022, but references 'all current and future IP'.
Question: Is there a temporal conflict that could void the IP transfer clause?
"""
result2 = router.execute_request(complex_query, user_tier="standard")

# Test Case 3: Premium user with simple query (should use Pro for quality guarantee)
result3 = router.execute_request(simple_query, user_tier="premium")
