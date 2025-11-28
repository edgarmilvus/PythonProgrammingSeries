
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

# Source File: theory_theoretical_foundations_part1.py
# Description: Theoretical Foundations
# ==========================================

# Example of unsafe data access in a robot controller
# If 'point' is missing, the robot crashes (KeyError)
# x_coord = parsed_json_object['point'][1]

# Example of safe data access using dict.get()
# If 'point' is missing, it defaults to [0, 0] or None, allowing the
# controller to log the error and safely abort or retry the maneuver.

def parse_robot_point(json_data):
    # Use dict.get() to safely retrieve the point list, defaulting to a safe
    # value (e.g., [0, 0] if coordinates are expected)
    point = json_data.get("point", [0, 0])
    label = json_data.get("label", "unknown_object")

    if point == [0, 0]:
        print(f"Warning: Failed to retrieve coordinates for {label}. Aborting grasp.")
        return None

    # Assuming [y, x] format
    y_norm = point[0]
    x_norm = point[1]
    return x_norm, y_norm, label
