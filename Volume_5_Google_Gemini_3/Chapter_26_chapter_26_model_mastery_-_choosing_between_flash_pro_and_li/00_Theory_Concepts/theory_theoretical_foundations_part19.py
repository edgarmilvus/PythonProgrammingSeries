
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

# Source File: theory_theoretical_foundations_part19.py
# Description: Theoretical Foundations
# ==========================================

def plot_model_distribution(
    optimizer: BudgetOptimizer,
    save_path: str = "model_distribution.png"
):
    """
    Shows what % of requests went to each model and the cost contribution.
    """
    stats = optimizer.get_stats()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Pie Chart 1: Request Distribution
    sizes = [stats['flash_usage_pct'], stats['pro_usage_pct']]
    labels = [f"Flash\n({stats['flash_usage_pct']:.1f}%)", 
              f"Pro\n({stats['pro_usage_pct']:.1f}%)"]
    colors = ['#2ecc71', '#e67e22']
    explode = (0.05, 0.05)
    
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
    ax1.set_title('Request Distribution by Model', fontsize=14, weight='bold', pad=20)
    
    # Pie Chart 2: Cost Contribution
    # Estimate: Flash requests are cheaper, but we need to calculate actual cost split
    flash_cost_contribution = (optimizer.flash_requests * optimizer.flash_cost * 1.0)
    pro_cost_contribution = (optimizer.pro_requests * optimizer.pro_cost * 1.0)
    total_cost = flash_cost_contribution + pro_cost_contribution
    
    if total_cost > 0:
        flash_cost_pct = (flash_cost_contribution / total_cost) * 100
        pro_cost_pct = (pro_cost_contribution / total_cost) * 100
    else:
        flash_cost_pct = pro_cost_pct = 50.0
    
    sizes2 = [flash_cost_pct, pro_cost_pct]
    labels2 = [f"Flash\n(${flash_cost_contribution:.2f})", 
               f"Pro\n(${pro_cost_contribution:.2f})"]
    
    ax2.pie(sizes2, explode=explode, labels=labels2, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
    ax2.set_title('Cost Contribution by Model', fontsize=14, weight='bold', pad=20)
    
    plt.suptitle(f'Model Usage Analysis\nTotal Requests: {stats["total_requests"]:,} | Total Cost: ${stats["current_spend"]:.2f}',
                 fontsize=16, weight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Model distribution visualization saved to {save_path}")
    plt.close()
