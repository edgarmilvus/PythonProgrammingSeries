
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

# llm_chain_subject_generator.py

import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- 1. CONFIGURATION AND SETUP ---

# CRITICAL: Replace 'YOUR_API_KEY_HERE' with your actual OpenAI key.
# In production, this should always be handled via environment variables.
# We set it here explicitly for demonstration purposes.
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY_HERE"

# --- 2. PROMPT DEFINITION ---

# Define the template string. This is the instruction set for the AI, 
# containing placeholders for dynamic content.
template = """
You are an expert copywriter specializing in professional email communication. 
Your task is to generate a single, concise, and high-impact subject line 
based on the provided context.

Topic: {topic}
Desired Tone: {tone}

Subject Line:
"""

# Create the PromptTemplate object. This object formalizes the structure 
# and explicitly defines the required input variables.
email_prompt = PromptTemplate(
    input_variables=["topic", "tone"],
    template=template,
)

# --- 3. MODEL INITIALIZATION ---

# Initialize the Language Model (LLM) instance.
# We use a standard OpenAI model wrapper.
# Temperature controls the creativity/randomness (0.0 is deterministic, 1.0 is highly creative).
llm = OpenAI(temperature=0.7, model_name="text-davinci-003")

# --- 4. CHAIN CREATION ---

# Instantiate the LLMChain. This step binds the specific PromptTemplate 
# to the specific LLM instance. This is the core workflow object.
subject_chain = LLMChain(llm=llm, prompt=email_prompt)

# --- 5. EXECUTION ---

# Define the dynamic input values for this specific run.
input_data = {
    "topic": "The Q3 budget review meeting scheduled for next Tuesday.",
    "tone": "Urgent and mandatory",
}

print("--- Input Parameters Supplied to the Chain ---")
print(f"Topic: {input_data['topic']}")
print(f"Tone: {input_data['tone']}\n")

# Execute the chain using the .run() method. 
# The chain automatically formats the prompt, sends the request, 
# and returns the final text response from the LLM.
try:
    response = subject_chain.run(input_data)

    print("--- Generated Output (Raw Text) ---")
    # LLMs often return output with leading/trailing whitespace or newlines.
    # We use .strip() for clean presentation.
    print(response.strip())

except Exception as e:
    print(f"\nAn error occurred during execution. Check your API key and connection.")
    print(f"Error details: {e}")

# Example Output (Actual output varies based on model and temperature):
# --- Generated Output (Raw Text) ---
# ACTION REQUIRED: Q3 Budget Review Scheduled for Tuesday - Mandatory Attendance
