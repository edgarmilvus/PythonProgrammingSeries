
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

# Source File: theory_theoretical_foundations_part3.py
# Description: Theoretical Foundations
# ==========================================

from google import genai
import time

client = genai.Client()

def benchmark_capability_threshold(test_set: List[Dict]) -> Dict:
    """
    Runs both Flash and Pro on the test set and calculates quality degradation.
    """
    results = {
        "flash": {"correct": 0, "total": 0, "by_complexity": {}},
        "pro": {"correct": 0, "total": 0, "by_complexity": {}}
    }
    
    for test_case in test_set:
        complexity = test_case["complexity"]
        prompt = test_case["prompt"]
        
        # Run Flash
        try:
            flash_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            # In production, you'd have an automated quality scorer or human eval
            flash_quality = evaluate_response_quality(flash_response.text, test_case["expected_output"])
            
            results["flash"]["total"] += 1
            if flash_quality > 0.8:  # 80% quality threshold
                results["flash"]["correct"] += 1
            
            # Track by complexity bucket
            if complexity not in results["flash"]["by_complexity"]:
                results["flash"]["by_complexity"][complexity] = {"correct": 0, "total": 0}
            results["flash"]["by_complexity"][complexity]["total"] += 1
            if flash_quality > 0.8:
                results["flash"]["by_complexity"][complexity]["correct"] += 1
                
        except Exception as e:
            print(f"Flash error: {e}")
        
        # Run Pro (same logic)
        try:
            pro_response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt
            )
            pro_quality = evaluate_response_quality(pro_response.text, test_case["expected_output"])
            
            results["pro"]["total"] += 1
            if pro_quality > 0.8:
                results["pro"]["correct"] += 1
            
            if complexity not in results["pro"]["by_complexity"]:
                results["pro"]["by_complexity"][complexity] = {"correct": 0, "total": 0}
            results["pro"]["by_complexity"][complexity]["total"] += 1
            if pro_quality > 0.8:
                results["pro"]["by_complexity"][complexity]["correct"] += 1
                
        except Exception as e:
            print(f"Pro error: {e}")
    
    return results

def evaluate_response_quality(response: str, expected: str) -> float:
    """
    Placeholder for quality evaluation.
    In production, use:
    - Human evaluation (gold standard)
    - LLM-as-a-judge (another model scores the output)
    - Automated metrics (BLEU, ROUGE for summarization; exact match for extraction)
    """
    # Simplified: keyword overlap
    response_words = set(response.lower().split())
    expected_words = set(expected.lower().split())
    overlap = len(response_words & expected_words) / max(len(expected_words), 1)
    return overlap
