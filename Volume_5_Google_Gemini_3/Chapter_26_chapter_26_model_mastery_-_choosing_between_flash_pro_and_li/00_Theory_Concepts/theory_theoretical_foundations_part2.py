
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

# Source File: theory_theoretical_foundations_part2.py
# Description: Theoretical Foundations
# ==========================================

import random
from typing import List, Dict

# Example: Legal document analysis test set
TEST_SET = [
    # Complexity Score: 10-30 (Simple)
    {"prompt": "Extract the parties' names from this 1-page NDA.", "complexity": 15, "expected_output": "Acme Corp, Beta Inc"},
    {"prompt": "What is the termination notice period in this employment contract?", "complexity": 20, "expected_output": "30 days"},
    
    # Complexity Score: 40-60 (Moderate)
    {"prompt": "Identify any non-compete clauses and their geographic scope.", "complexity": 50, "expected_output": "Non-compete: 50 miles from HQ, 2 years"},
    {"prompt": "Summarize the indemnification obligations in 3 bullet points.", "complexity": 55, "expected_output": "..."},
    
    # Complexity Score: 70-90 (High)
    {"prompt": "Analyze this merger agreement for contradictions between Section 4.2 and Section 9.7.", "complexity": 80, "expected_output": "Contradiction detected: ..."},
    {"prompt": "Assess the enforceability of this arbitration clause under NY law, considering recent precedent.", "complexity": 85, "expected_output": "..."},
]

def generate_stratified_test_set(num_samples: int = 100) -> List[Dict]:
    """
    Creates a balanced test set across complexity levels.
    In production, you'd pull this from real user queries with human-labeled difficulty.
    """
    test_set = []
    complexity_levels = [20, 40, 60, 80, 90]  # Stratified sampling
    
    for complexity in complexity_levels:
        for _ in range(num_samples // len(complexity_levels)):
            test_set.append({
                "complexity": complexity,
                "prompt": f"[Real user query at complexity {complexity}]",
                "expected_quality_score": 100 - complexity  # Simple tasks should have high quality
            })
    
    return test_set
