
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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

def configure_pipeline(source_file, mode="standard", output_type="json", verbose=False):
    """
    Configures a data processing pipeline with mandatory and optional settings.

    Args:
        source_file (str): The path to the required input file.
        mode (str, optional): The processing mode. Defaults to 'standard'.
        output_type (str, optional): The desired output format. Defaults to 'json'.
        verbose (bool, optional): Flag to enable detailed logging. Defaults to False.
    """
    print("\n--- Pipeline Configuration Summary ---")
    print(f"Source File: {source_file}")
    print(f"Processing Mode: {mode}")
    print(f"Output Format: {output_type}")
    print(f"Verbose Logging: {verbose}")
    print("--------------------------------------")


# 3. Basic Call (Providing only the required positional argument)
print("--- 3. Basic Call (Using all defaults) ---")
configure_pipeline("data/input.csv")

# 4. Customized Call (Mixed Arguments: Positional required, Keywords optional)
print("--- 4. Customized Call (Override mode and verbose) ---")
configure_pipeline("data/large_set.txt", mode="optimized", verbose=True)

# 5. Keyword-Only Override (Providing all arguments via keywords, changing only output_type)
print("--- 5. Keyword-Only Override (Changing output_type) ---")
configure_pipeline(source_file="data/archive.log", output_type="xml")
