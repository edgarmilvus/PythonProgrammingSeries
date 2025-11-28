
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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

# 1. Initialization
stability_score = 6
weather_condition = "Storm"  # Test cases: "Storm", "Clear", "Heavy Rain", ""
# stability_score = 11 # Test case for Data Error

advisory_level = ""

# 2. Input Validation (Rule 5): Preempt all other checks
if stability_score < 1 or stability_score > 10 or weather_condition == "":
    advisory_level = "DATA ERROR"
    advisory_description = "Input data is outside expected range or missing."

# 1. Extreme Danger (Level 4): Stability 3 or less
elif stability_score <= 3:
    advisory_level = "Level 4"
    advisory_description = "Extreme Danger: High political instability detected."

# 4. Low Risk (Level 1): Stability 8 or higher
elif stability_score >= 8:
    advisory_level = "Level 1"
    advisory_description = "Low Risk: Proceed with standard precautions."

# 3. High Risk (Level 3): Stability 4/5 OR (Stability 6/7 AND Bad Weather)
# Note: This handles the remaining scores (4, 5, 6, 7)
elif (stability_score == 4 or stability_score == 5) or \
     (stability_score >= 6 and stability_score <= 7 and weather_condition in ["Storm", "Heavy Rain"]):
    # Use backslash for line continuation for readability
    advisory_level = "Level 3"
    advisory_description = "High Risk: Exercise extreme caution due to instability or severe weather."

# 3. Moderate Risk (Level 2): This 'else' catches the only remaining possibility:
# Stability 6 or 7 AND weather is NOT Storm/Heavy Rain (i.e., Clear, Cloudy, Fog)
else:
    advisory_level = "Level 2"
    advisory_description = "Moderate Risk: Be vigilant, but conditions are generally manageable."

# Output
print(f"--- Travel Advisory System ---")
print(f"Stability Score: {stability_score}")
print(f"Weather: {weather_condition}")
print(f"Travel Advisory: {advisory_level} - {advisory_description}")
