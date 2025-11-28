
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

# Source File: theory_theoretical_foundations_part20.py
# Description: Theoretical Foundations
# ==========================================

def plot_quality_vs_cost_frontier(
    benchmark_data: List[Dict],
    save_path: str = "quality_cost_frontier.png"
):
    """
    Creates a scatter plot showing the Pareto frontier of quality vs cost.
    
    Args:
        benchmark_data: List of dicts with keys: 
            {"model": "flash", "complexity": 50, "quality": 0.85, "cost": 0.001}
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Separate Flash and Pro points
    flash_points = [d for d in benchmark_data if "flash" in d["model"].lower()]
    pro_points = [d for d in benchmark_data if "pro" in d["model"].lower()]
    
    # Extract coordinates
    flash_costs = [p["cost"] for p in flash_points]
    flash_quality = [p["quality"] * 100 for p in flash_points]  # Convert to percentage
    
    pro_costs = [p["cost"] for p in pro_points]
    pro_quality = [p["quality"] * 100 for p in pro_points]
    
    # Plot scatter
    ax.scatter(flash_costs, flash_quality, 
               s=150, c='green', alpha=0.6, edgecolors='black', linewidth=1.5,
               label='Flash Model', marker='o')
    
    ax.scatter(pro_costs, pro_quality, 
               s=150, c='orange', alpha=0.6, edgecolors='black', linewidth=1.5,
               label='Pro Model', marker='s')
    
    # Draw the Pareto frontier (optimal trade-off curve)
    # Combine all points and sort by cost
    all_points = sorted(benchmark_data, key=lambda x: x["cost"])
    frontier_costs = []
    frontier_quality = []
    max_quality_seen = 0
    
    for point in all_points:
        quality_pct = point["quality"] * 100
        if quality_pct > max_quality_seen:
            frontier_costs.append(point["cost"])
            frontier_quality.append(quality_pct)
            max_quality_seen = quality_pct
    
    ax.plot(frontier_costs, frontier_quality, 
            'k--', linewidth=2, alpha=0.5, label='Pareto Frontier (Optimal Trade-off)')
    
    # Formatting
    ax.set_xlabel('Cost per Request ($)', fontsize=13, weight='bold')
    ax.set_ylabel('Quality Score (%)', fontsize=13, weight='bold')
    ax.set_title('Quality vs. Cost Trade-off Analysis\nThe Efficiency Frontier',
                 fontsize=16, weight='bold', pad=20)
    ax.legend(loc='lower right', fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add capability threshold annotation
    ax.axhline(y=90, color='red', linestyle=':', linewidth=2, alpha=0.7)
    ax.text(max(flash_costs + pro_costs) * 0.7, 91, 
            'Quality Threshold (90%)', 
            fontsize=11, color='red', weight='bold')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Quality vs cost frontier saved to {save_path}")
    plt.close()

# Example usage
example_benchmark_data = [
    {"model": "flash", "complexity": 20, "quality": 0.95, "cost": 0.001},
    {"model": "flash", "complexity": 50, "quality": 0.88, "cost": 0.0012},
    {"model": "flash", "complexity": 70, "quality": 0.75, "cost": 0.0015},
    {"model": "pro", "complexity": 20, "quality": 0.98, "cost": 0.010},
    {"model": "pro", "complexity": 50, "quality": 0.96, "cost": 0.012},
    {"model": "pro", "complexity": 70, "quality": 0.94, "cost": 0.015},
]

plot_quality_vs_cost_frontier(example_benchmark_data)
