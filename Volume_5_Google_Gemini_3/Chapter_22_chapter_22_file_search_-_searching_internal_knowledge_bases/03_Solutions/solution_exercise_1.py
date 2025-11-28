
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

# Source File: solution_exercise_1.py
# Description: Solution for Exercise 1
# ==========================================

# --- Setup: Create necessary local files for RAG exercises ---
import os
import uuid
from google import genai
from google.genai import types
from google.genai.errors import APIError
import time

# 1. Document for Exercise 1 (Basic Upload)
EX1_CONTENT = """
The concept of the 'Digital Twin' is central to modern industrial IoT.
A Digital Twin is a virtual representation that serves as the real-time digital counterpart of a physical object or process.
It allows engineers to run simulations, predict failures, and optimize performance before making changes to the physical asset.
This technology is predominantly used in manufacturing, healthcare, and large-scale infrastructure management.
"""
with open("ex1_doc.txt", "w") as f:
    f.write(EX1_CONTENT)

# 2. Document for Exercise 3 (Chunking Test)
# This document contains a distinct, short answer embedded within a larger block.
EX3_CONTENT = """
Project Chronos Report Summary:
The initial phase focused on optimizing latency for edge devices.
The primary finding was that utilizing a 5G mesh network reduced average query time by 45 milliseconds.
However, the secondary objective, which involved power consumption reduction, proved challenging.
The final recommendation for the next quarter is to prioritize hardware-level optimization over software refactoring.
"""
with open("ex3_doc.txt", "w") as f:
    f.write(EX3_CONTENT)

# 3. Documents for Exercise 4 (Metadata Filtering Challenge)
# Document A: Focuses on historical context, tagged as 'History'.
EX4_CONTENT_A = """
Document ID: 9001-A | Title: Origins of the Quantum Computer
The theoretical basis for quantum computing was first proposed by physicists in the early 1980s,
notably by Paul Benioff and Richard Feynman. They suggested that classical computers could not efficiently
simulate quantum mechanical systems, necessitating a new computational paradigm.
"""
with open("ex4_doc_a.txt", "w") as f:
    f.write(EX4_CONTENT_A)

# Document B: Focuses on modern applications, tagged as 'Current'.
EX4_CONTENT_B = """
Document ID: 9001-B | Title: Modern Applications in Qubit Technology
Today, quantum systems are primarily used for drug discovery, financial modeling, and materials science.
Superconducting qubits, trapped ions, and photonic systems represent the leading hardware architectures currently under development.
"""
with open("ex4_doc_b.txt", "w") as f:
    f.write(EX4_CONTENT_B)

print("Local setup files created successfully.")
# --- End of Setup ---
