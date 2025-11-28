
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

# This code block illustrates the difference in prompt design 
# for Chain of Thought (CoT) versus Native Reasoning (Zero-Shot CoT).
# Assume the necessary 'google-genai' client setup is complete.

# Define a complex prompt that requires multiple calculation steps
MATH_PROBLEM = (
    "A baker starts the day with 20 kg of dough. "
    "He uses 40% of the dough to make large loaves and 5 kg to make small rolls. "
    "If the remaining dough is split evenly into 10 medium baguettes, "
    "how many grams of dough are in each medium baguette? "
    "Provide the final answer in grams."
)

# --- 1. Chain of Thought (CoT) Prompting ---
# Objective: Maximize verifiability and transparency, sacrificing speed.
# We explicitly force the model to generate its intermediate steps.
cot_prompt = f"""
TASK: Solve the following problem. You must act as a meticulous instructor.
1. First, calculate the amount of dough used for large loaves (in kg).
2. Next, calculate the remaining dough after making small rolls (in kg).
3. Finally, determine the weight of a single medium baguette (in grams).

Show all your calculations and reasoning step-by-step before stating the final answer.

Problem: {MATH_PROBLEM}
"""

# --- 2. Native Reasoning (Zero-Shot CoT) Prompting ---
# Objective: Maximize efficiency and minimize token output.
# We rely on Gemini's native reasoning capability to perform the steps internally.
# The prompt focuses entirely on constraints and the final output format (Zero-Shot).
native_prompt = f"""
TASK: Solve the following problem efficiently. 
You must provide ONLY the final numerical value of the weight in grams. 
Do not include any steps, units, explanations, or introductory phrases.

Problem: {MATH_PROBLEM}
"""

# Example of how the prompts would be used in a highly constrained API call
def generate_response(model_client, prompt_text, method_name):
    """
    Simulates calling the Gemini API with the specified prompt configuration.
    Note: temperature is kept at 1.0 as recommended for reasoning tasks.
    """
    # In a real scenario, this would be:
    # response = model_client.models.generate_content(
    #     model='gemini-2.5-pro',  # Use a powerful reasoning model
    #     contents=prompt_text,
    #     config={"temperature": 1.0, "max_output_tokens": 1024}
    # )
    # return response.text
    
    # Placeholder for demonstration purposes:
    if "meticulous instructor" in prompt_text:
        return (
            "Step 1: Calculate large loaves: 20 kg * 40% = 8 kg.\n"
            "Step 2: Calculate remaining dough: 20 kg - 8 kg - 5 kg = 7 kg.\n"
            "Step 3: Calculate single baguette weight: 7 kg / 10 = 0.7 kg.\n"
            "Step 4: Convert to grams: 0.7 kg * 1000 = 700 grams.\n"
            "The final answer is 700 grams."
        )
    else:
        return "700"

# # Execution comparison (Conceptual Output)
# print("--- Chain of Thought (High Latency/Cost, High Transparency) ---")
# print(generate_response(None, cot_prompt, "CoT"))
# print("\n" + "="*50 + "\n")
# print("--- Native Reasoning (Low Latency/Cost, Low Transparency) ---")
# print(generate_response(None, native_prompt, "Native"))
# # Output: 700 (Ready for direct software consumption)
