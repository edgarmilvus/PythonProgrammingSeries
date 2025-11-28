
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

# 1. Initial String Definition
dna_sequence = "GATTACA_AGTCG_TACCGA_CATTGA_CGTTA"

# 2. Length Determination
sequence_length = len(dna_sequence)
print(f"Total Length: {sequence_length}")

# 3. Extraction Tasks (Slicing)

# Segment A: First 7 characters (indices 0 up to 7)
segment_a = dna_sequence[:7]

# Segment B: Starting from the 9th character (index 8) up to, but not including, the 14th (index 14)
segment_b = dna_sequence[8:14]

# Segment C: The last five characters using negative indexing
segment_c = dna_sequence[-5:]

# Segment D: Reversing the entire sequence using the step parameter [::-1]
segment_d = dna_sequence[::-1]

# 4. Concatenation and Output
# Combining segments A, B, and C with a hyphen separator
combined_analysis = segment_a + "-" + segment_b + "-" + segment_c

print(f"Combined Analysis: {combined_analysis}")
print(f"Reversed Sequence: {segment_d}")
