
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

# Source File: solution_exercise_4.py
# Description: Solution for Exercise 4
# ==========================================

def plan_trip(preference, budget, duration_days):
    """
    Recommends a travel destination based on preference, budget, and duration.
    """
    print(f"\n--- Planning Trip: Preference={preference}, Budget=${budget}, Duration={duration_days} days ---")
    recommendation = ""

    # Primary Classification: Preference
    if preference == "Beach":
        # Secondary Classification: Budget
        if budget > 3000:
            recommendation = "Luxury Caribbean Resort."
        elif budget >= 1000:  # Implies 1000 to 3000
            recommendation = "Mid-Range Coastal Town."
        else:  # Budget < 1000
            recommendation = "Local Camping Trip."

    elif preference == "Mountain":
        # Secondary Classification: Duration
        if duration_days > 7:
            recommendation = "Extended Hiking Expedition."
        else:  # Duration <= 7 days
            recommendation = "Weekend Cabin Getaway."

    elif preference == "City":
        # Secondary Classification: Budget and Duration combined
        if budget > 2000 and duration_days < 5:
            recommendation = "Fast-Paced European Capital Tour."
        else:
            recommendation = "Domestic Cultural City Break."

    # Unknown Preference
    else:
        recommendation = "Preference not recognized. Please choose Beach, Mountain, or City."

    print(f"Recommendation: {recommendation}")

# Example Usage:
plan_trip("Beach", 4500, 7)    # Luxury Caribbean Resort
plan_trip("Mountain", 1500, 10) # Extended Hiking Expedition
plan_trip("City", 2500, 3)     # Fast-Paced European Capital Tour
plan_trip("City", 1500, 8)     # Domestic Cultural City Break
plan_trip("Desert", 1000, 5)   # Unknown Preference
