
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

# Source File: project_advanced_application_script.py
# Description: Advanced Application Script
# ==========================================

import os
import json
from typing import Dict, Any

# Assuming LangChain components are available from previous installations
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

# --- 1. Configuration and Mock Data Setup ---

# Set up a mock environment variable for API key (Required for ChatOpenAI initialization)
# In a real application, this would be loaded from .env or OS environment
os.environ["OPENAI_API_KEY"] = "MOCK_KEY_FOR_DEMO" 

# Simulate an internal inventory database (read-only access for the agent)
INVENTORY_DB: Dict[str, Dict[str, Any]] = {
    "P-4001": {"name": "Quantum Processor", "stock": 150, "unit_price": 450.00, "location": "Warehouse A"},
    "P-4002": {"name": "Flux Capacitor", "stock": 25, "unit_price": 1200.50, "location": "Warehouse B"},
    "P-4003": {"name": "Aether Converter", "stock": 500, "unit_price": 15.99, "location": "Warehouse A"},
}

# --- 2. Pydantic Schemas for Tool Input Validation ---

class InventoryCheckInput(BaseModel):
    """Input schema for checking current stock levels."""
    product_id: str = Field(description="The unique identifier (e.g., P-4001) of the product whose stock level needs checking.")

class ValuationCalculationInput(BaseModel):
    """Input schema for calculating the total value of a specific quantity of a product."""
    product_id: str = Field(description="The unique identifier (e.g., P-4001) of the product.")
    quantity: int = Field(description="The specific quantity of the product to calculate the value for. Must be a positive integer.")

# --- 3. Custom Tool Definitions using the @tool Decorator ---

@tool(args_schema=InventoryCheckInput)
def check_inventory_stock(product_id: str) -> str:
    """
    Checks the current available stock level and location for a given product ID in the internal inventory system.
    Returns a JSON string containing the product name, stock, and location if found.
    """
    if product_id in INVENTORY_DB:
        data = INVENTORY_DB[product_id]
        return json.dumps({
            "product_name": data["name"],
            "current_stock": data["stock"],
            "location": data["location"]
        })
    else:
        return f"Error: Product ID '{product_id}' not found in the inventory database."

@tool(args_schema=ValuationCalculationInput)
def calculate_inventory_valuation(product_id: str, quantity: int) -> str:
    """
    Calculates the total monetary value of a specified quantity of a product.
    Requires the product ID and the specific quantity to be valued.
    """
    if product_id not in INVENTORY_DB:
        return f"Error: Product ID '{product_id}' not found for valuation calculation."
    
    if quantity <= 0:
        return "Error: Quantity must be a positive integer for valuation calculation."

    data = INVENTORY_DB[product_id]
    unit_price = data["unit_price"]
    total_value = unit_price * quantity
    
    return f"The total value of {quantity} units of {data['name']} (ID: {product_id}) is ${total_value:,.2f}."

# --- 4. Agent Initialization and Execution ---

# Aggregate the custom tools
logistics_tools = [check_inventory_stock, calculate_inventory_valuation]

# Initialize the LLM (Using a mock setup since we don't need actual API calls for tool demonstration)
# Note: In a real scenario, the LLM must be capable of function calling/tool use.
llm = ChatOpenAI(temperature=0, model="gpt-4o", openai_api_key=os.environ["OPENAI_API_KEY"])

# Define the Agent Prompt (crucial for guiding the agent's reasoning process - ReAct)
template = """
You are an expert Logistics and Inventory Agent. Your sole purpose is to answer queries 
related to product stock and financial valuation using the provided tools. 
You must strictly follow the Thought/Action/Observation pattern.

Query: {input}
{agent_scratchpad}
"""
prompt = PromptTemplate.from_template(template)

# Create the ReAct Agent
agent = create_react_agent(llm, logistics_tools, prompt)

# Create the Agent Executor
agent_executor = AgentExecutor(agent=agent, tools=logistics_tools, verbose=True)

# Define a complex query that requires sequential tool use
complex_query = "I need to know the current stock level and location of the Flux Capacitor (P-4002). Then, calculate the total value if we were to sell 10 units of it."

print("\n--- Running Complex Agent Query ---")
agent_executor.invoke({"input": complex_query})

