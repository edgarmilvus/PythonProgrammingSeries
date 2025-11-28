
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

# Source File: solution_exercise_3.py
# Description: Solution for Exercise 3
# ==========================================

#!/usr/bin/env python3
# This is the required Shebang Line

import sys
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- Configuration ---
# Ensure environment variable OPENAI_API_KEY is set
if 'OPENAI_API_KEY' not in os.environ:
    print("Error: OPENAI_API_KEY environment variable not set.")
    sys.exit(1)

# --- Argument Parsing (Requirement 1 & 2) ---
# sys.argv[0] is the script name, so we expect 3 total arguments.
if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <topic> <complexity_level>")
    sys.exit(1)

# Map command-line arguments to variables
topic = sys.argv[1]
complexity_level = sys.argv[2]

# --- LangChain Setup ---
# 1. Initialize LLM
llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")

# 2. Define Prompt Template
template = (
    "You are a world-class technical explainer. Your task is to explain the "
    "concept of '{topic}' to a '{complexity_level}' audience. "
    "Ensure the explanation is accurate, uses appropriate analogies for the level, "
    "and includes a brief, commented Python code example demonstrating the concept."
    "\n\nExplanation:"
)

prompt = PromptTemplate(
    input_variables=["topic", "complexity_level"],
    template=template
)

# 3. Create LLMChain
explainer_chain = LLMChain(llm=llm, prompt=prompt)

# --- Execution (Requirement 3) ---
print(f"--- Generating Explanation for '{topic}' (Level: {complexity_level}) ---")

try:
    # Pass the command-line inputs directly to the chain
    response = explainer_chain.invoke(
        {"topic": topic, "complexity_level": complexity_level}
    )

    # Note: Using .invoke() returns a dictionary in the latest LangChain
    print("\n" + response['text'])

except Exception as e:
    print(f"\nAn error occurred during chain execution: {e}")
    sys.exit(1)

# --- End of Script ---
