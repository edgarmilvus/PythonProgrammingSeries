
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

import os
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- 1. Define the Schema ---
class FutureValueInput(BaseModel):
    """Input schema for calculating the Future Value of an investment."""
    principal: float = Field(description="The starting principal amount in currency units (e.g., 10000.00).")
    annual_rate: float = Field(description="The annual interest rate, expressed as a decimal (e.g., 0.05 for 5%).")
    years: int = Field(description="The duration of the investment in full years.")

# --- 2 & 3. Define the Tool Function and LangChain Tool ---
@tool(args_schema=FutureValueInput)
def calculate_future_value(principal: float, annual_rate: float, years: int) -> str:
    """
    Calculates the Future Value (FV) of an investment using compound interest.
    Formula: FV = Principal * (1 + Rate)^Years.
    """
    try:
        # Check for valid inputs before calculation
        if principal < 0 or annual_rate < 0 or years < 0:
            return "Error: Principal, rate, and years must be non-negative."
            
        fv = principal * (1 + annual_rate) ** years
        return f"The Future Value after {years} years is: ${fv:,.2f}"
    except Exception as e:
        return f"Error during calculation: {e}"

# --- 4. Testing Setup and Execution ---
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini") 
tools = [calculate_future_value]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a specialized financial analyst agent. Use the provided tools to calculate financial metrics."),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("--- Test 1: Valid Prompt (Numeric Input) ---")
valid_prompt = "If I invest $10,000 at 5% interest for 10 years, what will the final value be?"
agent_executor.invoke({"input": valid_prompt})

print("\n--- Test 2: Invalid Prompt (Natural Language Conversion Required) ---")
invalid_prompt = "Calculate FV for ten thousand dollars, five percent, and a decade."
# The agent must correctly convert "ten thousand dollars" -> 10000.0, "five percent" -> 0.05, and "a decade" -> 10.
agent_executor.invoke({"input": invalid_prompt})
