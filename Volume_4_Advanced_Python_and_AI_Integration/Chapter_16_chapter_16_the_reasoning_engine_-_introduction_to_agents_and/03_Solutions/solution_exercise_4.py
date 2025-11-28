
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

from typing import Dict, Callable

# --- Tool Definitions ---

def CalculatorTool(expression: str) -> str:
    """
    Performs simple arithmetic calculations (addition, subtraction, multiplication, division).
    Input must be a mathematical expression string (e.g., '10 / 2.5').
    """
    try:
        # Safer evaluation is assumed in a real scenario
        result = eval(expression)
        return str(result)
    except Exception:
        return "Calculation Error: Invalid mathematical expression."

def SearchTool(query: str) -> str:
    """
    Provides general knowledge, current events, or non-specific data like average temperatures.
    Use this for non-financial, non-calculative queries.
    """
    if "average daily temperature in London last week" in query.lower():
        return "The average daily temperature in London last week was 18.5 degrees Celsius."
    if "analyst sentiment regarding NVDA's last earnings report" in query.lower():
        return "General analyst sentiment for NVDA's last earnings report was overwhelmingly positive, citing strong data center growth."
    return f"Search result for '{query}': General knowledge found."

def FinancialDataTool(ticker_symbol: str) -> str:
    """
    Specifically retrieves the current closing price for a given stock ticker symbol (e.g., 'NVDA', 'GOOG').
    Input must be the ticker symbol string.
    """
    ticker_symbol = ticker_symbol.upper()
    prices = {"NVDA": 950.25, "MSFT": 420.00, "GOOG": 175.50}
    
    if ticker_symbol in prices:
        return f"The current closing price for {ticker_symbol} is ${prices[ticker_symbol]:.2f}."
    return f"Financial Data Error: Ticker symbol {ticker_symbol} not found or price unavailable."

# --- Agent Toolset ---
AGENT_TOOLS: Dict[str, Callable] = {
    "CalculatorTool": CalculatorTool,
    "SearchTool": SearchTool,
    "FinancialDataTool": FinancialDataTool
}

# --- Simulation of Agent Steps (Orchestration) ---

# Query: "What is the result of dividing the current price of NVDA by the average daily temperature in London last week, 
# and what was the general analyst sentiment regarding NVDA's last earnings report?"

print("--- Agent Orchestration Simulation ---")

# 1. Agent Thought: Need NVDA price (FinancialDataTool)
action_1_name = "FinancialDataTool"
action_1_input = "NVDA"
obs_1 = FinancialDataTool(action_1_input)
print(f"Action 1: {action_1_name}({action_1_input}) -> Observation: {obs_1}")
# Extracted NVDA Price: 950.25

# 2. Agent Thought: Need London temperature (SearchTool)
action_2_name = "SearchTool"
action_2_input = "average daily temperature in London last week"
obs_2 = SearchTool(action_2_input)
print(f"Action 2: {action_2_name}({action_2_input}) -> Observation: {obs_2}")
# Extracted Temp: 18.5

# 3. Agent Thought: Perform the division (CalculatorTool)
# Input derived from Obs 1 and Obs 2: '950.25 / 18.5'
action_3_name = "CalculatorTool"
action_3_input = "950.25 / 18.5"
obs_3 = CalculatorTool(action_3_input)
print(f"Action 3: {action_3_name}({action_3_input}) -> Observation: {obs_3}")
# Result: 51.36486486486486

# 4. Agent Thought: Need analyst sentiment (SearchTool)
action_4_name = "SearchTool"
action_4_input = "general analyst sentiment regarding NVDA's last earnings report"
obs_4 = SearchTool(action_4_input)
print(f"Action 4: {action_4_name}({action_4_input}) -> Observation: {obs_4}")

# 5. Agent Final Answer Synthesis
final_answer = (
    f"\nFinal Answer: The result of the division is approximately {float(obs_3):.2f}. "
    f"Regarding the analyst sentiment, it was {obs_4.split(': ')[1]}"
)
print(final_answer)
