
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

# Exercise 8-5: Boolean Simplification Challenge

# 1. Define variables (Test Data)
has_config = True
is_default_profile = False
is_read_only_mode = True

# 2. Calculate the verbose baseline
# Original Logic: (has_config == True and is_default_profile == False) or 
#                 (is_read_only_mode == True and has_config != False)
should_load_config_verbose = (has_config == True and is_default_profile == False) or \
                             (is_read_only_mode == True and has_config != False)

# 3. Write the simplified expression
# Simplified Logic: (has_config AND NOT is_default_profile) OR (is_read_only_mode AND has_config)
# Factoring out 'has_config': has_config AND (NOT is_default_profile OR is_read_only_mode)

should_load_config_simplified = has_config and (not is_default_profile or is_read_only_mode)

# 4. Print results
print(f"Variable Values: has_config={has_config}, is_default_profile={is_default_profile}, is_read_only_mode={is_read_only_mode}")
print("-" * 40)
print(f"Result (Verbose Logic): {should_load_config_verbose}")
print(f"Result (Simplified Logic): {should_load_config_simplified}")
print(f"Do the results match? {should_load_config_verbose == should_load_config_simplified}")
