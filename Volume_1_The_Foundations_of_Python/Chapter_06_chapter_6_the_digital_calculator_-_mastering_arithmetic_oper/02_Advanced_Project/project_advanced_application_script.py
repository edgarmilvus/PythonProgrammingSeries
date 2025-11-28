
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

# ----------------------------------------------------------------------
# Pallet Optimization and Shipping Cost Calculator
# Demonstrates: Floor Division (//), Modulus (%), Multiplication (*), Addition (+)
# Chapter 6: Mastering Arithmetic Operators
# ----------------------------------------------------------------------

# --- 1. System Constants and Rates ---

# Define the maximum number of units that fit on one standard pallet (the divisor)
PALLET_CAPACITY = 480

# Define the average weight of a single unit (in kilograms)
UNIT_WEIGHT_KG = 0.75

# Define the base shipping cost per full, optimized pallet
COST_PER_FULL_PALLET = 155.50

# Define the handling surcharge for each loose, unpalletized unit (higher rate due to manual handling)
COST_PER_LOOSE_UNIT = 0.65

# --- 2. Input Data ---

# Total number of units received in the shipment batch (the dividend)
total_units_received = 15730

# --- 3. Core Calculation: Pallet Allocation using Advanced Arithmetic ---

# Calculate the number of full pallets required using Floor Division (//).
# This operator discards the fractional part, giving us only the whole number of completed pallets.
num_full_pallets = total_units_received // PALLET_CAPACITY

# Calculate the number of leftover units using the Modulus Operator (%).
# This operator returns the remainder after division, representing items that don't fill a pallet.
leftover_units = total_units_received % PALLET_CAPACITY

# Determine if a partial pallet is strictly necessary for inventory tracking.
# If the remainder is greater than zero, we need one additional pallet (even if partially empty).
needs_partial_pallet = 1 if leftover_units > 0 else 0

# Calculate the total number of physical pallets needed (full + 1 for the remainder).
total_pallets_needed = num_full_pallets + needs_partial_pallet

# --- 4. Weight Calculations using Multiplication and Addition ---

# Calculate the total gross weight of all units using simple Multiplication (*)
total_gross_weight_kg = total_units_received * UNIT_WEIGHT_KG

# Calculate the weight specifically dedicated to the full pallets
weight_full_pallets_kg = num_full_pallets * PALLET_CAPACITY * UNIT_WEIGHT_KG

# Calculate the weight of the loose (leftover) units
weight_loose_units_kg = leftover_units * UNIT_WEIGHT_KG

# Verification check: Ensure the sum of parts equals the total (Addition)
weight_check = weight_full_pallets_kg + weight_loose_units_kg

# --- 5. Cost Calculations ---

# Calculate the base cost for shipping the full, efficient pallets
cost_full_pallets = num_full_pallets * COST_PER_FULL_PALLET

# Calculate the surcharge for handling the less efficient loose units
cost_loose_unit_surcharge = leftover_units * COST_PER_LOOSE_UNIT

# Calculate the final total shipping cost (Addition)
total_shipping_cost = cost_full_pallets + cost_loose_unit_surcharge

# --- 6. Output Summary and Formatting ---

print("=" * 70)
print("LOGISTICS SHIPMENT REPORT: Efficient Pallet Optimization")
print("=" * 70)

# Display Input Data
print(f"Input Units Received: {total_units_received:,}")
print(f"Standard Pallet Capacity: {PALLET_CAPACITY} units")
print("-" * 70)

# Display Pallet Allocation Results
print("--- Allocation Summary ---")
print(f"1. Full Pallets Required (using //): {num_full_pallets}")
print(f"2. Leftover Units (using %):         {leftover_units}")
print(f"3. Total Physical Pallets Used:      {total_pallets_needed}")
print("-" * 70)

# Display Weight Metrics
print("--- Weight Metrics ---")
print(f"Unit Weight: {UNIT_WEIGHT_KG:.2f} kg")
print(f"Total Gross Weight: {total_gross_weight_kg:.2f} kg")
print(f"Weight of Full Pallets Load: {weight_full_pallets_kg:.2f} kg")
print(f"Weight of Loose Load:        {weight_loose_units_kg:.2f} kg")
print(f"Weight Verification Check: {weight_check:.2f} kg (Match: {weight_check == total_gross_weight_kg})")
print("-" * 70)

# Display Financial Summary
print("--- Financial Summary ---")
print(f"Rate Per Full Pallet: ${COST_PER_FULL_PALLET:.2f}")
print(f"Surcharge Per Loose Unit: ${COST_PER_LOOSE_UNIT:.2f}")
print("")
print(f"Cost of Full Pallets: ${cost_full_pallets:.2f}")
print(f"Surcharge for Loose Units: ${cost_loose_unit_surcharge:.2f}")
print("--------------------")
print(f"FINAL TOTAL SHIPPING COST: ${total_shipping_cost:.2f}")
print("=" * 70)
