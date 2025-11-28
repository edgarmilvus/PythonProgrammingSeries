
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

# Original Configuration Variables
site_title = "The Python Foundation Guide"
site_version = 1.0
copyright_year = 2024

# 1. Define New Variables (Requirement 1)
theme_color = "dark_mode"
max_users = 500

# Generating the output string (simulating template rendering)
config_output = "--- Site Configuration ---\n"
config_output += f"Title: {site_title}\n"
config_output += f"Version: {site_version}\n"

# 2. Integrate New Variables (Requirement 2)
# Append the new configuration settings to the output string
config_output += f"Theme Color: {theme_color}\n"
config_output += f"Maximum Users: {max_users}\n"

# Finish the output
config_output += f"Copyright: (C) {copyright_year}\n"
config_output += "--------------------------"

# 3. Execution (Requirement 3)
print(config_output)
