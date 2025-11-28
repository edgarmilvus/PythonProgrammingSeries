
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

# Source File: theory_theoretical_foundations_part18.py
# Description: Theoretical Foundations
# ==========================================

def plot_budget_burn_rate(
    optimizer: BudgetOptimizer,
    days: int = 30,
    save_path: str = "budget_burn_rate.png"
):
    """
    Simulates and plots the budget consumption over a month.
    Shows if you're on track or overspending.
    """
    # Simulate day-by-day spending
    daily_spend = []
    cumulative_spend = []
    ideal_cumulative = []
    
    daily_budget = optimizer.monthly_budget / days
    
    for day in range(1, days + 1):
        # Simulate daily requests (assuming uniform distribution)
        daily_requests = 8_000_000 // days
        
        # Simulate spending for this day
        day_cost = 0
        for _ in range(daily_requests):
            import random
            complexity = random.choice([20, 40, 60, 80])
            tokens = random.randint(100, 2000)
            is_premium = random.random() < 0.10
            
            model = optimizer.route_request(tokens, complexity, is_premium)
            cost_per_1k = optimizer.flash_cost if "flash" in model else optimizer.pro_cost
            day_cost += (tokens / 1000) * cost_per_1k
        
        daily_spend.append(day_cost)
        cumulative_spend.append(sum(daily_spend))
        ideal_cumulative.append(daily_budget * day)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 7))
    
    days_array = np.arange(1, days + 1)
    
    # Plot actual spending
    ax.plot(days_array, cumulative_spend, 
            linewidth=2.5, color='red', label='Actual Spending', marker='o', markersize=4)
    
    # Plot ideal spending (linear)
    ax.plot(days_array, ideal_cumulative, 
            linewidth=2, color='green', linestyle='--', label='Ideal Linear Spend')
    
    # Plot budget limit
    ax.axhline(y=optimizer.monthly_budget, 
               color='black', linestyle='-', linewidth=2, label='Monthly Budget Cap')
    
    # Fill area between actual and ideal
    ax.fill_between(days_array, cumulative_spend, ideal_cumulative, 
                     where=(np.array(cumulative_spend) > np.array(ideal_cumulative)),
                     color='red', alpha=0.2, label='Overspending')
    
    ax.fill_between(days_array, cumulative_spend, ideal_cumulative, 
                     where=(np.array(cumulative_spend) <= np.array(ideal_cumulative)),
                     color='green', alpha=0.2, label='Under Budget')
    
    # Formatting
    ax.set_xlabel('Day of Month', fontsize=12, weight='bold')
    ax.set_ylabel('Cumulative Spend ($)', fontsize=12, weight='bold')
    ax.set_title('Budget Burn Rate Analysis\nAre We On Track?', fontsize=16, weight='bold')
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add annotations
    final_spend = cumulative_spend[-1]
    if final_spend > optimizer.monthly_budget:
        status = "⚠️ OVER BUDGET"
        color = 'red'
    else:
        status = "✅ WITHIN BUDGET"
        color = 'green'
    
    ax.text(days * 0.5, optimizer.monthly_budget * 0.9, 
            f"Final Status: {status}\nProjected Spend: ${final_spend:,.2f}",
            fontsize=12, weight='bold', color=color,
            bbox=dict(boxstyle='round', facecolor='white', edgecolor=color, linewidth=2))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Burn rate visualization saved to {save_path}")
    plt.close()
