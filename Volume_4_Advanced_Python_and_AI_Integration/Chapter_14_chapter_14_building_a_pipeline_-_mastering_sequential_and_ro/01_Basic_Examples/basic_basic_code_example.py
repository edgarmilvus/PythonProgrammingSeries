
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

# Source File: basic_basic_code_example.py
# Description: Basic Code Example
# ==========================================

from langchain_community.llms import OpenAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate
import os
import warnings

# Suppress deprecation warnings for cleaner output
warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- 0. Setup and Initialization ---
# NOTE: Replace 'os.environ["OPENAI_API_KEY"]' with your actual setup method.
# We are using a placeholder LLM initialization here for demonstration.
try:
    # Initialize the LLM
    # We use a lower temperature for slightly more deterministic results
    llm = OpenAI(temperature=0.7) 
except Exception as e:
    # Handle environment key not set (common in textbook examples)
    print(f"Warning: LLM initialization failed. Ensure API key is set. Error: {e}")
    # In a real scenario, this would halt execution.

# --- 1. Define Chain 1: Style Transformation ---
# This chain takes the raw idea and transforms its tone.
prompt_c1 = PromptTemplate(
    input_variables=["input_idea"],
    template="Rewrite the following concept in the dramatic, exaggerated style of a 1940s radio announcer, ensuring the output is verbose: {input_idea}"
)
# Create the first LLMChain instance
chain_1 = LLMChain(llm=llm, prompt=prompt_c1)

# --- 2. Define Chain 2: Action Extraction ---
# This chain takes the verbose, styled text (output of Chain 1) and condenses it.
prompt_c2 = PromptTemplate(
    # NOTE ON SIMPLE SEQUENTIAL CHAIN: 
    # The variable name used here ('styled_text') is arbitrary 
    # and only used internally by this specific PromptTemplate. 
    # SimpleSequentialChain ignores this name and simply passes the 
    # previous chain's full output as the sole input to this chain.
    input_variables=["styled_text"], 
    template="From the following highly dramatic text, extract the single, most important actionable command and present it as a concise, one-sentence instruction: {styled_text}"
)
# Create the second LLMChain instance
chain_2 = LLMChain(llm=llm, prompt=prompt_c2)

# --- 3. Pipeline Construction: SimpleSequentialChain ---
# The SimpleSequentialChain links the chains in the order provided.
overall_chain = SimpleSequentialChain(
    chains=[chain_1, chain_2],
    verbose=True # Crucial for debugging and observing intermediate steps
)

# --- 4. Execution ---
initial_input = "Hey team, maybe we should look at getting the budget numbers finalized sometime next week, if everyone is free."
print(f"\n--- Initial Informal Input ---\n'{initial_input}'")

# Run the entire pipeline with the initial input
# The .run() method handles passing the intermediate results automatically.
try:
    final_output = overall_chain.run(initial_input)

    print("\n\n--- Final Actionable Output ---")
    print(final_output)

except Exception as e:
    # Catches errors if the LLM setup failed (e.g., API key missing)
    print(f"\nExecution Error: Failed to run chain. Details: {e}")

