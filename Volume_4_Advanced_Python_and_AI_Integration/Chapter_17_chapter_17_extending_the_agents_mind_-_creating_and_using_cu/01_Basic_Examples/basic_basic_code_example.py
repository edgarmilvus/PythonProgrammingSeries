
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

import os
from typing import Dict, Any
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv

# --- 0. Setup and Mock Data ---
# Load environment variables (API keys)
load_dotenv() 

# Mock external data source (e.g., a database query result)
INVENTORY = {
    "widget_a": 15.50, 
    "gizmo_b": 22.75, 
    "module_c": 50.00
}

# --- 1. Defining the Custom Tool ---
@tool
def get_product_price(product_name: str) -> float:
    """
    Retrieves the current selling price of a specified product 
    from the internal inventory system. 
    
    Input must be the exact product name (e.g., 'widget_a', 'gizmo_b').
    Returns 0.0 if the product name is not found in the inventory.
    """
    # Standardize input for robust lookup
    normalized_name = product_name.lower().strip()
    
    # Use dict.get() for safe access, returning 0.0 as the default if not found
    price = INVENTORY.get(normalized_name, 0.0)
    
    return price

# --- 2. Agent Initialization and Integration ---

# Initialize the LLM (requires OPENAI_API_KEY set in environment)
# We use a robust model capable of function calling
try:
    llm = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo")
except Exception as e:
    print(f"Error initializing LLM: {e}. Ensure API key is set.")
    exit()

# Package the custom tool(s) into a list
custom_tools = [get_product_price]

# Initialize the Agent Executor
# AgentType.OPENAI_FUNCTIONS is highly effective for tool usage
agent_executor = initialize_agent(
    tools=custom_tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True # Set to True to see the LLM's reasoning and tool calls
)

# --- 3. Execution ---

# Define a query that requires both tool usage and general knowledge
query = "What is the price of a gizmo_b? Also, what is the capital of France?"

print(f"\n--- Executing Agent with Custom Tool ---\n")

# Run the agent
response = agent_executor.invoke({"input": query})

print(f"\n--- Final Agent Response ---\n")
print(response['output'])
