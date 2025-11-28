
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

# Source File: project_advanced_application_script.py
# Description: Advanced Application Script
# ==========================================

import json
import os
from typing import Dict, Any, Tuple, Set, List

# --- Configuration and Setup ---

# Define the output directory for reports, using a standard library path constant
OUTPUT_DIR = "dependency_reports"

def setup_environment(data_dev: Dict[str, Any], data_prod: Dict[str, Any]) -> Tuple[Set[str], Set[str]]:
    """
    Initializes the environment, ensures the output directory exists,
    and extracts dependency lists, converting them immediately to sets.
    """
    # 1. Use os.path functions for robust, platform-independent directory handling
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

    # 2. Extract dependency lists (assuming 'dependencies' key exists)
    # Convert lists to sets immediately for efficient processing and uniqueness guarantee.
    dev_deps = set(data_dev.get("dependencies", []))
    prod_deps = set(data_prod.get("dependencies", []))

    print(f"\n[INFO] Development Dependencies Found: {len(dev_deps)} unique items.")
    print(f"[INFO] Production Dependencies Found: {len(prod_deps)} unique items.")

    return dev_deps, prod_deps

def analyze_dependencies(dev_set: Set[str], prod_set: Set[str]) -> Dict[str, List[str]]:
    """
    Performs the core set theory analysis to compare the two dependency sets.
    This function utilizes the concise Python set operators.
    """
    print("\n[ANALYSIS] Performing Set Operations...")

    # A. Intersection (&): Libraries required by BOTH environments (common ground)
    common = dev_set & prod_set

    # B. Difference (-): Libraries unique to Development (Dev-only tools)
    dev_only = dev_set - prod_set

    # C. Difference (.difference()): Libraries unique to Production (Prod-only tools)
    # Using the method form for demonstration variety
    prod_only = prod_set.difference(dev_set)

    # D. Union (|): All unique libraries across the entire project scope
    all_unique = dev_set | prod_set

    # E. Symmetric Difference (^): Libraries required by one environment but not the other (mismatches)
    mismatched = dev_set ^ prod_set

    # Package results, converting sets back to sorted lists for predictable JSON output
    results = {
        "common_dependencies": sorted(list(common)),
        "dev_only_dependencies": sorted(list(dev_only)),
        "prod_only_dependencies": sorted(list(prod_only)),
        "all_unique_dependencies": sorted(list(all_unique)),
        "mismatched_dependencies": sorted(list(mismatched))
    }
    return results

def generate_report(analysis_results: Dict[str, List[str]]):
    """
    Writes the analysis results to a structured JSON file using the json module.
    """
    # Construct the full output path using os.path.join for safety
    output_path = os.path.join(OUTPUT_DIR, "dependency_report.json")

    try:
        # Use a context manager ('with open') for safe file handling (Pythonic practice)
        with open(output_path, 'w', encoding='utf-8') as f:
            # Serialize the Python dictionary into a JSON string and write it to the file
            json.dump(analysis_results, f, indent=4)
        
        print(f"\n[SUCCESS] Analysis complete. Report saved to: {output_path}")

        # Print summary statistics derived from the lengths of the resulting sets/lists
        print("\n--- Summary Statistics ---")
        print(f"Total Unique Dependencies (Union): {len(analysis_results['all_unique_dependencies'])}")
        print(f"Dependencies Common to Both (Intersection): {len(analysis_results['common_dependencies'])}")
        print(f"Dependencies Mismatched (Symmetric Difference): {len(analysis_results['mismatched_dependencies'])}")
        print(f"Dev-Only Dependencies (Potential cleanup): {len(analysis_results['dev_only_dependencies'])}")

    except IOError as e:
        print(f"[ERROR] Could not write report to {output_path}: {e}")


# --- Simulated Data Input (Representing parsed configuration files) ---
DEV_CONFIG = {
    "project_name": "Phoenix_API",
    "environment": "Development",
    "dependencies": [
        "requests", "numpy", "pandas", "flask", "gunicorn", "pytest", "mock", "black", "mypy"
    ]
}

PROD_CONFIG = {
    "project_name": "Phoenix_API",
    "environment": "Production",
    "dependencies": [
        "requests", "numpy", "pandas", "flask", "gunicorn", "supervisor", "prometheus", "mypy"
    ]
}


# --- Main Execution Block ---
if __name__ == "__main__":
    print("--- Dependency Set Analyzer Initialized ---")

    # Step 1: Setup and Data Extraction
    dev_deps_set, prod_deps_set = setup_environment(DEV_CONFIG, PROD_CONFIG)

    # Step 2: Core Set Theory Analysis
    report_data = analyze_dependencies(dev_deps_set, prod_deps_set)

    # Step 3: Reporting and Output Generation
    generate_report(report_data)
