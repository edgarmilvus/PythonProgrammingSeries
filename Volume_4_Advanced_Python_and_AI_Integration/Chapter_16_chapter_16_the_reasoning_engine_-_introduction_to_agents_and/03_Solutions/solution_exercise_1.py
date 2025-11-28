
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

import re
from typing import Dict, Callable, Any

# --- Tool Definitions ---

def get_weather(city: str) -> str:
    """Mock tool: Returns weather information for a given city."""
    if "london" in city.lower():
        return "The weather in London is currently 15C and rainy."
    return f"Weather data for {city} is unavailable."

def add_numbers(input_str: str) -> str:
    """Mock tool: Adds two comma-separated numbers from a string."""
    try:
        # Assuming input_str is 'num1, num2'
        parts = [float(p.strip()) for p in input_str.split(',')]
        if len(parts) == 2:
            return str(parts[0] + parts[1])
        return "Error: Requires exactly two comma-separated numbers."
    except ValueError:
        return "Error: Invalid input format for addition."

MOCK_TOOLS: Dict[str, Callable[[str], str]] = {
    "get_weather": get_weather,
    "add_numbers": add_numbers
}

def simulate_react_step(llm_output: str) -> str:
    """
    Parses LLM output for ReAct components, executes the action, and returns the observation.
    Returns 'COMPLETED' if the final answer is found.
    """
    # 1. Check for Final Answer
    if "Final Answer:" in llm_output:
        return "COMPLETED"

    # 2. Parsing Logic
    # Regex to find Action: (word characters)
    action_match = re.search(r"Action:\s*(\w+)", llm_output, re.IGNORECASE)
    # Regex to find Action Input: (everything following, including newlines)
    input_match = re.search(r"Action Input:\s*(.*)", llm_output, re.DOTALL | re.IGNORECASE)

    if not action_match:
        return "Observation: No valid Action found. LLM must specify an Action or Final Answer."

    action_name = action_match.group(1).strip()
    # Clean up input, removing leading/trailing whitespace
    action_input = input_match.group(1).strip() if input_match else ""

    # 3. Execution and Observation
    if action_name not in MOCK_TOOLS:
        return f"Observation: Tool '{action_name}' not found or invalid."

    try:
        tool_func = MOCK_TOOLS[action_name]
        
        # Execute the tool with the parsed string input
        result = tool_func(action_input)

        return f"Observation: {result}"

    except Exception as e:
        # Catch unexpected errors during tool execution
        return f"Observation: Tool execution failed with error: {type(e).__name__} - {str(e)}"

# --- Demonstration ---
print("--- Test 1: Successful Addition ---")
llm_turn_1 = "Thought: I need to calculate the sum of 10 and 5.\nAction: add_numbers\nAction Input: 10, 5"
obs_1 = simulate_react_step(llm_turn_1)
print(f"LLM Output:\n{llm_turn_1}\n\nExecutor Response:\n{obs_1}\n")

print("--- Test 2: Invalid Action ---")
llm_turn_2 = "Thought: I need to check the stock price.\nAction: get_stock_price\nAction Input: GOOG"
obs_2 = simulate_react_step(llm_turn_2)
print(f"LLM Output:\n{llm_turn_2}\n\nExecutor Response:\n{obs_2}\n")

print("--- Test 3: Completion ---")
llm_turn_3 = "Thought: I have the final result.\nFinal Answer: The sum is 15.0"
obs_3 = simulate_react_step(llm_turn_3)
print(f"LLM Output:\n{llm_turn_3}\n\nExecutor Response:\n{obs_3}")
