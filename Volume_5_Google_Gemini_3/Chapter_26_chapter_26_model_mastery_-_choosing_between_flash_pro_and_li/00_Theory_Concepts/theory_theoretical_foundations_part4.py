
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

# Source File: theory_theoretical_foundations_part4.py
# Description: Theoretical Foundations
# ==========================================

def find_capability_threshold(benchmark_results: Dict) -> int:
    """
    Analyzes benchmark results to find where Flash's accuracy drops below acceptable.
    
    Returns:
        The complexity score where Flash accuracy falls below 90% (upgrade threshold)
    """
    print("\n--- Capability Threshold Analysis ---")
    print("Complexity | Flash Accuracy | Pro Accuracy | Upgrade Recommended?")
    print("-" * 70)
    
    threshold_complexity = 100  # Default: always use Pro
    
    for complexity in sorted(benchmark_results["flash"]["by_complexity"].keys()):
        flash_data = benchmark_results["flash"]["by_complexity"][complexity]
        pro_data = benchmark_results["pro"]["by_complexity"][complexity]
        
        flash_accuracy = flash_data["correct"] / flash_data["total"] if flash_data["total"] > 0 else 0
        pro_accuracy = pro_data["correct"] / pro_data["total"] if pro_data["total"] > 0 else 0
        
        upgrade = "YES" if flash_accuracy < 0.90 else "NO"
        
        print(f"{complexity:^10} | {flash_accuracy:^14.1%} | {pro_accuracy:^12.1%} | {upgrade:^20}")
        
        # The threshold is the first complexity level where Flash drops below 90%
        if flash_accuracy < 0.90 and threshold_complexity == 100:
            threshold_complexity = complexity
    
    print(f"\n🎯 CAPABILITY THRESHOLD IDENTIFIED: Complexity Score {threshold_complexity}")
    print(f"   Recommendation: Use Flash for scores < {threshold_complexity}, Pro for scores >= {threshold_complexity}")
    
    return threshold_complexity
