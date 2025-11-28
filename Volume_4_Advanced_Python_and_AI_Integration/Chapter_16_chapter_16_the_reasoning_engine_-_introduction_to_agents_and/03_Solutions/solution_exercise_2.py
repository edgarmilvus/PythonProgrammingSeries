
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

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import json

# 1. State Backend
class MemoryStore:
    """Simple in-memory key-value store for string data."""
    def __init__(self):
        self._store: Dict[str, str] = {}

    def store(self, key: str, value: str) -> str:
        """Stores the value associated with the key."""
        self._store[key] = value
        return f"Successfully stored '{value}' under key: {key}"

    def retrieve(self, key: str) -> str:
        """Retrieves the stored value."""
        return self._store.get(key, f"Error: Key '{key}' not found in memory store.")

# 2. Input Schemas (Pydantic Models)
class StoreInput(BaseModel):
    """Schema for storing data."""
    key: str = Field(description="The unique string key to store the data under.")
    value: str = Field(description="The string value (e.g., a numerical result) to be stored.")

class RetrieveInput(BaseModel):
    """Schema for retrieving data."""
    key: str = Field(description="The unique key (string) to retrieve the data from.")

# 3. Custom Tool Class (Simulating LangChain's BaseTool structure)
class MemoryStoreTool:
    name = "Memory_Store"
    description = (
        "A critical tool for persistent storage and retrieval of intermediate data. "
        "Use 'store' to save numerical results or context, and 'retrieve' to fetch them later. "
        "Always provide inputs as a JSON string matching the required schema."
    )
    # Initialize the state instance
    _store_instance = MemoryStore()

    def store(self, key: str, value: str) -> str:
        """Stores a string value associated with a key."""
        return self._store_instance.store(key, value)
    
    def retrieve(self, key: str) -> str:
        """Retrieves the stored string value associated with a key."""
        return self._store_instance.retrieve(key)

# Mocking other required tools
def CalculatorTool(expression: str) -> str:
    """Calculates the result of a simple mathematical expression."""
    try:
        # Use eval cautiously; in a real tool, use a safer math parser
        result = eval(expression)
        return str(result)
    except Exception:
        return "Calculation Error: Invalid expression."

def SearchTool(query: str) -> str:
    """Searches for general knowledge or current events."""
    if "inflation rate" in query.lower():
        return "The current US inflation rate (CPI) is 3.5% as of the latest report."
    return f"Search result for '{query}': General context found."

# --- Simulation of Agent Steps (Focusing on MemoryStore) ---

# Agent Goal: Calculate $450 * 1.15$, store it as 'budget', find inflation, and combine.

# Step 1: Calculate and Store
calculator_result = CalculatorTool("450 * 1.15") # Result: 517.5
print(f"Step 1 (Calculator): Result is {calculator_result}")

# LLM Action Input for Store: {"key": "budget", "value": "517.5"}
store_key = "budget"
store_value = calculator_result
store_observation = MemoryStoreTool().store(store_key, store_value)
print(f"Step 1 (Store Observation): {store_observation}")

# Step 2: Search for Inflation
search_query = "current year's inflation rate in the US"
search_observation = SearchTool(search_query)
print(f"\nStep 2 (Search Observation): {search_observation}")

# Step 3: Retrieve the stored budget
retrieve_key = "budget"
retrieve_observation = MemoryStoreTool().retrieve(retrieve_key)
print(f"\nStep 3 (Retrieve Observation): {retrieve_observation}")

# Step 4: Final Synthesis (LLM combines: 517.5 + 3.5%)
print("\nStep 4 (Final Thought): LLM uses 517.5 (retrieved) and 3.5% (searched) to form the final answer.")
