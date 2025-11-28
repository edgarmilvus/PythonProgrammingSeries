
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

# Source File: theory_theoretical_foundations_part1.py
# Description: Theoretical Foundations
# ==========================================

# The Capability Threshold Decision Function

def should_upgrade_to_pro(
    task_complexity_score: float,
    flash_error_rate: float,
    error_cost_per_incident: float,
    flash_cost_per_request: float,
    pro_cost_per_request: float
) -> bool:
    """
    Determines if upgrading to Pro is economically justified.
    
    Args:
        task_complexity_score: 0-100 scale (0=trivial, 100=expert-level)
        flash_error_rate: Historical failure rate for this complexity (0.0-1.0)
        error_cost_per_incident: Business cost of a wrong answer (e.g., $500 for legal errors)
        flash_cost_per_request: Cost to use Flash model
        pro_cost_per_request: Cost to use Pro model
    
    Returns:
        True if Pro is justified, False if Flash is acceptable
    """
    # Expected cost with Flash = (Model Cost) + (Error Rate × Error Cost)
    flash_total_cost = flash_cost_per_request + (flash_error_rate * error_cost_per_incident)
    
    # Expected cost with Pro (assume 95% reduction in errors due to superior reasoning)
    pro_error_rate = flash_error_rate * 0.05  # Pro is 20x more reliable for complex tasks
    pro_total_cost = pro_cost_per_request + (pro_error_rate * error_cost_per_incident)
    
    # Upgrade if Pro's total cost (including prevented errors) is lower
    return pro_total_cost < flash_total_cost
