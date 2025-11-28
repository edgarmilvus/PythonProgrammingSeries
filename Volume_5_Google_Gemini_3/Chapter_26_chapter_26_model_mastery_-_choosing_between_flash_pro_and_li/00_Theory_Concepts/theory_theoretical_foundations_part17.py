
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

# Source File: theory_theoretical_foundations_part17.py
# Description: Theoretical Foundations
# ==========================================

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List

def plot_model_comparison_triangle(
    flash_metrics: Dict[str, float],
    pro_metrics: Dict[str, float],
    save_path: str = "model_comparison_triangle.png"
):
    """
    Creates a radar/spider chart showing the three-way trade-off.
    
    Args:
        flash_metrics: {"cost": 1.0, "latency": 0.8, "quality": 85.0}
        pro_metrics: {"cost": 10.0, "latency": 2.5, "quality": 97.0}
    """
    categories = ['Cost\n(Lower is Better)', 'Latency\n(Lower is Better)', 'Quality\n(Higher is Better)']
    
    # Normalize all metrics to 0-100 scale for comparison
    # Cost: Invert (lower is better) and normalize
    flash_cost_norm = 100 - (flash_metrics["cost"] / max(flash_metrics["cost"], pro_metrics["cost"]) * 100)
    pro_cost_norm = 100 - (pro_metrics["cost"] / max(flash_metrics["cost"], pro_metrics["cost"]) * 100)
    
    # Latency: Invert (lower is better) and normalize
    flash_latency_norm = 100 - (flash_metrics["latency"] / max(flash_metrics["latency"], pro_metrics["latency"]) * 100)
    pro_latency_norm = 100 - (pro_metrics["latency"] / max(flash_metrics["latency"], pro_metrics["latency"]) * 100)
    
    # Quality: Direct (higher is better)
    flash_quality_norm = flash_metrics["quality"]
    pro_quality_norm = pro_metrics["quality"]
    
    flash_values = [flash_cost_norm, flash_latency_norm, flash_quality_norm]
    pro_values = [pro_cost_norm, pro_latency_norm, pro_quality_norm]
    
    # Number of variables
    num_vars = len(categories)
    
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # Complete the loop
    flash_values += flash_values[:1]
    pro_values += pro_values[:1]
    angles += angles[:1]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Plot Flash
    ax.plot(angles, flash_values, 'o-', linewidth=2, label='Gemini 2.5 Flash', color='green')
    ax.fill(angles, flash_values, alpha=0.25, color='green')
    
    # Plot Pro
    ax.plot(angles, pro_values, 'o-', linewidth=2, label='Gemini 2.5 Pro', color='orange')
    ax.fill(angles, pro_values, alpha=0.25, color='orange')
    
    # Fix axis to go in the right order and start at 12 o'clock
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw axis lines for each angle and label
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=12)
    
    # Set y-axis limits and labels
    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(['25', '50', '75', '100'], size=10)
    ax.set_rlabel_position(180)
    
    # Add legend and title
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)
    plt.title('Model Selection Trade-off Analysis\n(Normalized Scores)', 
              size=16, weight='bold', pad=20)
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Save
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Visualization saved to {save_path}")
    plt.close()

# Example usage
flash_metrics = {
    "cost": 1.0,      # Relative cost per request
    "latency": 0.65,  # Average latency in seconds
    "quality": 87.0   # Quality score (0-100)
}

pro_metrics = {
    "cost": 10.0,
    "latency": 2.3,
    "quality": 96.0
}

plot_model_comparison_triangle(flash_metrics, pro_metrics)
