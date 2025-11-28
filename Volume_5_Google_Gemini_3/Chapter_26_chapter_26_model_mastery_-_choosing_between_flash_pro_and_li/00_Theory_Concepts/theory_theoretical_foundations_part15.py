
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

# Source File: theory_theoretical_foundations_part15.py
# Description: Theoretical Foundations
# ==========================================

import time
from datetime import datetime, timedelta
from typing import Optional

class BudgetOptimizer:
    """
    A production-grade model router that enforces budget constraints
    while maintaining quality thresholds.
    """
    
    def __init__(
        self,
        monthly_budget: float,
        flash_cost_per_1k_tokens: float = 0.075,  # Input cost
        pro_cost_per_1k_tokens: float = 1.25,
        quality_threshold: float = 0.92  # Minimum acceptable accuracy
    ):
        self.monthly_budget = monthly_budget
        self.flash_cost = flash_cost_per_1k_tokens
        self.pro_cost = pro_cost_per_1k_tokens
        self.quality_threshold = quality_threshold
        
        # Runtime state
        self.current_spend = 0.0
        self.month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        self.total_requests = 0
        self.flash_requests = 0
        self.pro_requests = 0
        self.flash_errors = 0
        self.pro_errors = 0
        
        # Dynamic thresholds
        self.emergency_mode = False
        
    def days_remaining_in_month(self) -> int:
        """Calculates days left in the current billing cycle."""
        today = datetime.now()
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        return (next_month - today).days
    
    def budget_utilization_rate(self) -> float:
        """Returns what % of the budget has been spent."""
        return self.current_spend / self.monthly_budget
    
    def time_utilization_rate(self) -> float:
        """Returns what % of the month has passed."""
        total_days = 30  # Simplified
        days_passed = 30 - self.days_remaining_in_month()
        return days_passed / total_days
    
    def is_overspending(self) -> bool:
        """
        Detects if we're spending faster than the month is progressing.
        Example: If 60% of budget is spent but only 40% of month has passed, we're overspending.
        """
        return self.budget_utilization_rate() > self.time_utilization_rate()
    
    def flash_error_rate(self) -> float:
        """Calculates the historical error rate for Flash."""
        if self.flash_requests == 0:
            return 0.0
        return self.flash_errors / self.flash_requests
    
    def route_request(
        self,
        estimated_input_tokens: int,
        complexity_score: int,
        is_premium_user: bool = False
    ) -> str:
        """
        The core routing logic with budget awareness.
        
        Returns:
            "gemini-2.5-flash" or "gemini-2.5-pro"
        """
        
        # RULE 1: Premium users always get Pro (business requirement)
        if is_premium_user:
            return "gemini-2.5-pro"
        
        # RULE 2: Emergency mode (budget nearly exhausted)
        if self.current_spend >= self.monthly_budget * 0.95:
            self.emergency_mode = True
            print("[ALERT] Budget 95% exhausted. EMERGENCY MODE: Flash only.")
            return "gemini-2.5-flash"
        
        # RULE 3: Overspending detection (spend faster than time)
        if self.is_overspending():
            print(f"[WARNING] Overspending detected: {self.budget_utilization_rate():.1%} budget spent, "
                  f"{self.time_utilization_rate():.1%} of month passed.")
            
            # Increase Flash usage percentage to slow spending
            # Only upgrade to Pro if complexity is VERY high (>80)
            if complexity_score < 80:
                print("[COST-SAVE] Routing to Flash to control burn rate.")
                return "gemini-2.5-flash"
        
        # RULE 4: Quality safety net
        # If Flash error rate exceeds threshold, force Pro even if expensive
        if self.flash_error_rate() > (1 - self.quality_threshold):
            print(f"[QUALITY-ALERT] Flash error rate {self.flash_error_rate():.1%} exceeds threshold. Forcing Pro.")
            return "gemini-2.5-pro"
        
        # RULE 5: Normal operation - complexity-based routing
        # Use the capability threshold concept from Section A
        capability_threshold = 65
        
        if complexity_score >= capability_threshold:
            return "gemini-2.5-pro"
        else:
            return "gemini-2.5-flash"
    
    def record_request(
        self,
        model_used: str,
        actual_tokens: int,
        had_error: bool
    ):
        """
        Updates internal state after a request completes.
        """
        self.total_requests += 1
        
        # Calculate cost
        cost_per_1k = self.flash_cost if "flash" in model_used else self.pro_cost
        request_cost = (actual_tokens / 1000) * cost_per_1k
        self.current_spend += request_cost
        
        # Track model usage
        if "flash" in model_used:
            self.flash_requests += 1
            if had_error:
                self.flash_errors += 1
        else:
            self.pro_requests += 1
            if had_error:
                self.pro_errors += 1
        
        # Log warnings
        if self.current_spend > self.monthly_budget:
            print(f"[CRITICAL] Budget exceeded! Spent: ${self.current_spend:.2f} / ${self.monthly_budget:.2f}")
    
    def get_stats(self) -> dict:
        """Returns current statistics for monitoring."""
        return {
            "total_requests": self.total_requests,
            "current_spend": self.current_spend,
            "budget_remaining": self.monthly_budget - self.current_spend,
            "budget_utilization": self.budget_utilization_rate(),
            "time_utilization": self.time_utilization_rate(),
            "flash_usage_pct": (self.flash_requests / self.total_requests * 100) if self.total_requests > 0 else 0,
            "pro_usage_pct": (self.pro_requests / self.total_requests * 100) if self.total_requests > 0 else 0,
            "flash_error_rate": self.flash_error_rate(),
            "emergency_mode": self.emergency_mode
        }
