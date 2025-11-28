
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

# --- Configuration Constants ---
# Base rates are determined by the distance zone.
BASE_RATE_ZONE_A = 5.00     # Local (1 day)
BASE_RATE_ZONE_B = 12.50    # Regional (3 days)
BASE_RATE_ZONE_C = 25.00    # National (7 days)
BASE_RATE_ZONE_D = 45.00    # International (14 days)

# Surcharges based on weight tiers.
SURCHARGE_HEAVY = 20.00     # For items > 15 kg
SURCHARGE_MEDIUM = 8.00     # For items > 5 kg
SURCHARGE_LIGHT = 0.00      # For items <= 5 kg

# Membership benefits.
DISCOUNT_PREMIUM = 0.15     # 15% off for premium members

# --- Core Logic Function ---
def calculate_shipping_cost(weight_kg: float, distance_zone: str, is_premium_member: bool) -> tuple:
    """
    Calculates the final shipping cost and estimated delivery time 
    based on zone, weight, and membership status using sequential elif checks.
    
    Returns: (final_cost, delivery_days)
    """
    
    # 1. Initialization and sanitization
    base_cost = 0.0
    surcharge = 0.0
    delivery_days = 0
    distance_zone = distance_zone.upper() # Standardize input case

    print(f"\n--- Calculating Rate for Zone {distance_zone}, Weight {weight_kg} kg ---")

    # --- Section A: Determining Base Rate and Delivery Time (Primary Elif Chain) ---
    # This chain is mutually exclusive. A package can only belong to one zone.
    if distance_zone == 'A':
        base_cost = BASE_RATE_ZONE_A
        delivery_days = 1
        print(f"-> Zone A detected. Base cost set to ${base_cost:.2f}.")
    elif distance_zone == 'B':
        base_cost = BASE_RATE_ZONE_B
        delivery_days = 3
        print(f"-> Zone B detected. Base cost set to ${base_cost:.2f}.")
    elif distance_zone == 'C':
        base_cost = BASE_RATE_ZONE_C
        delivery_days = 7
        print(f"-> Zone C detected. Base cost set to ${base_cost:.2f}.")
    elif distance_zone == 'D':
        base_cost = BASE_RATE_ZONE_D
        delivery_days = 14
        print(f"-> Zone D detected. Base cost set to ${base_cost:.2f}.")
    else:
        # The final 'else' handles invalid or unsupported zone inputs.
        print(f"ERROR: Invalid distance zone '{distance_zone}'. Calculation aborted.")
        return (0.0, 0)

    # --- Section B: Applying Weight Surcharge (Secondary Elif Chain) ---
    # CRITICAL: The order must be descending (heaviest first) to ensure correctness.
    if weight_kg > 15.0:
        # Very heavy items (e.g., industrial equipment)
        surcharge = SURCHARGE_HEAVY
        delivery_days += 2 # Add two days for specialized handling
        print(f"-> Applied HEAVY surcharge: +${surcharge:.2f}")
    elif weight_kg > 5.0:
        # Medium weight items (e.g., large boxes)
        surcharge = SURCHARGE_MEDIUM
        print(f"-> Applied MEDIUM surcharge: +${surcharge:.2f}")
    else:
        # Light items (e.g., documents, small parcels)
        surcharge = SURCHARGE_LIGHT
        print("-> Item is LIGHT. No weight surcharge applied.")

    # 2. Calculate Subtotal before discount
    subtotal = base_cost + surcharge
    final_cost = subtotal
    discount_applied = 0.0

    # --- Section C: Applying Membership Discount (Independent If) ---
    # This check is independent of the zone and weight logic.
    if is_premium_member:
        discount_applied = subtotal * DISCOUNT_PREMIUM
        final_cost = subtotal - discount_applied
        
        # Premium perk: Expedited handling time (minimum 1 day)
        delivery_days = max(1, delivery_days - 1)
        
        print(f"-> Premium Discount Applied ({DISCOUNT_PREMIUM*100:.0f}%): -${discount_applied:.2f}")
        print(f"-> Premium Expedited Delivery: {delivery_days} day(s)")
        
    # 3. Return results
    return (round(final_cost, 2), delivery_days)

# --- Simulation Data and Execution ---

shipments_to_process = [
    ("Light Standard, Zone A", 2.5, "A", False),    # Cheapest path
    ("Heavy Premium, Zone C", 18.0, "C", True),     # Complex path: Heavy surcharge, Premium discount
    ("Medium Standard, Zone B", 7.0, "B", False),   # Medium path
    ("Very Heavy Standard, Zone D", 30.0, "D", False), # Most expensive base path
    ("Invalid Zone Test", 4.0, "Z", True)           # Error path (Else block test)
]

print("==================================================")
print("LOGISTICAL PRICING SERVICE STARTUP")
print("==================================================")

for description, weight, zone, premium in shipments_to_process:
    
    cost, days = calculate_shipping_cost(weight, zone, premium)
    
    print("-" * 50)
    if cost > 0.0:
        print(f"SUMMARY: {description}")
        print(f"  TOTAL COST: ${cost:.2f}")
        print(f"  ESTIMATED DELIVERY: {days} day(s)")
    else:
        print(f"SUMMARY: {description} failed due to input error.")
    print("=" * 50)

