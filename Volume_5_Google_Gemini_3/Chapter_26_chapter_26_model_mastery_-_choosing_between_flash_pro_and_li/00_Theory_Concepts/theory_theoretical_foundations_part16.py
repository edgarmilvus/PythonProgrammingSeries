
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

# Source File: theory_theoretical_foundations_part16.py
# Description: Theoretical Foundations
# ==========================================

def simulate_month(optimizer: BudgetOptimizer, total_requests: int = 8_000_000):
    """
    Simulates a full month of traffic with varying complexity.
    """
    import random
    
    print(f"\n{'='*60}")
    print(f"SIMULATION: Processing {total_requests:,} requests")
    print(f"Budget: ${optimizer.monthly_budget:,.2f}")
    print(f"{'='*60}\n")
    
    for i in range(total_requests):
        # Simulate varying complexity (most requests are simple, few are complex)
        complexity = random.choices(
            population=[20, 40, 60, 80],
            weights=[50, 30, 15, 5]  # 50% simple, 5% expert
        )[0]
        
        # Simulate token usage
        estimated_tokens = random.randint(100, 2000)
        
        # Simulate premium users (10% of traffic)
        is_premium = random.random() < 0.10
        
        # Route the request
        model = optimizer.route_request(
            estimated_input_tokens=estimated_tokens,
            complexity_score=complexity,
            is_premium_user=is_premium
        )
        
        # Simulate actual usage (add output tokens)
        actual_tokens = estimated_tokens + random.randint(50, 500)
        
        # Simulate errors (Flash has higher error rate for complex tasks)
        if "flash" in model and complexity > 70:
            error_chance = 0.15  # 15% error rate on complex tasks
        elif "flash" in model:
            error_chance = 0.02  # 2% baseline
        else:
            error_chance = 0.01  # Pro is more reliable
        
        had_error = random.random() < error_chance
        
        # Record the result
        optimizer.record_request(model, actual_tokens, had_error)
        
        # Print periodic updates
        if (i + 1) % 1_000_000 == 0:
            stats = optimizer.get_stats()
            print(f"\n[Checkpoint: {i+1:,} requests]")
            print(f"  Spend: ${stats['current_spend']:,.2f} ({stats['budget_utilization']:.1%} of budget)")
            print(f"  Flash: {stats['flash_usage_pct']:.1%} | Pro: {stats['pro_usage_pct']:.1%}")
            print(f"  Flash Error Rate: {stats['flash_error_rate']:.2%}")
            
            if optimizer.emergency_mode:
                print("  ⚠️  EMERGENCY MODE ACTIVE")
    
    # Final report
    stats = optimizer.get_stats()
    print(f"\n{'='*60}")
    print("FINAL REPORT")
    print(f"{'='*60}")
    print(f"Total Requests: {stats['total_requests']:,}")
    print(f"Final Spend: ${stats['current_spend']:,.2f}")
    print(f"Budget Status: ${stats['budget_remaining']:,.2f} {'UNDER' if stats['budget_remaining'] > 0 else 'OVER'} budget")
    print(f"Model Distribution: Flash {stats['flash_usage_pct']:.1f}% | Pro {stats['pro_usage_pct']:.1f}%")
    print(f"Quality Metrics: Flash Error Rate {stats['flash_error_rate']:.2%}")
    print(f"Emergency Mode Triggered: {'YES' if stats['emergency_mode'] else 'NO'}")
    
    # Success criteria
    success = (
        stats['budget_remaining'] >= 0 and 
        stats['flash_error_rate'] < 0.10 and
        stats['total_requests'] == total_requests
    )
    
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: ", end="")
    if success:
        print("Served all requests within budget while maintaining quality.")
    else:
        if stats['budget_remaining'] < 0:
            print(f"Budget exceeded by ${abs(stats['budget_remaining']):,.2f}")
        if stats['flash_error_rate'] >= 0.10:
            print(f"Quality degraded (Flash error rate: {stats['flash_error_rate']:.1%})")
    
    return success

# Run the simulation
if __name__ == "__main__":
    # Scenario: $5,000 budget, 8M requests/month
    optimizer = BudgetOptimizer(
        monthly_budget=5000.0,
        flash_cost_per_1k_tokens=0.075,
        pro_cost_per_1k_tokens=1.25,
        quality_threshold=0.92
    )
    
    success = simulate_month(optimizer, total_requests=8_000_000)
    
    if not success:
        print("\n[CHALLENGE] Adjust the routing logic in route_request() to pass the test!")
