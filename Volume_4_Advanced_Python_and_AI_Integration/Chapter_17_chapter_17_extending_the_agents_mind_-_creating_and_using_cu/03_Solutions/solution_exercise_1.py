
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

import asyncio
from typing import Literal
from pydantic import BaseModel, Field, ValidationError
from langchain.tools import tool

# --- Exercise 1: The Secure Configuration Validator Tool ---

class ConfigKeyRequest(BaseModel):
    """Schema for requesting a specific configuration key."""
    key_name: str = Field(..., description="The exact name of the configuration key to retrieve.")

@tool(args_schema=ConfigKeyRequest)
def read_config_key(key_name: str) -> str:
    """
    Retrieves secure configuration values from the internal system. 
    
    WARNING: This tool is strictly limited to retrieving only the following keys: 
    'database_url', 'api_timeout', or 'service_port'. 
    If you request any other key, the tool will fail and provide an error message. 
    Always use the exact key name as listed.
    """
    allowed_keys = {
        "database_url": "postgres://user:pass@db.internal:5432/main",
        "api_timeout": "15 seconds",
        "service_port": "8080"
    }
    
    if key_name in allowed_keys:
        # Simulate a quick lookup
        return f"Successfully retrieved configuration for {key_name}: {allowed_keys[key_name]}"
    else:
        # Crucial feedback for the LLM to understand its limitation
        allowed_list = ', '.join(f"'{k}'" for k in allowed_keys.keys())
        return (f"Error: Key '{key_name}' is not accessible via this tool. "
                f"Only the following keys are permitted: {allowed_list}.")

# --- Exercise 2: The Complex Data Transformation Tool with Strict Constraints ---

class InvestmentParameters(BaseModel):
    """
    Strict schema for financial calculations, enforcing positive values 
    and ensuring the rate is provided as a decimal between 0 and 1.
    """
    principal_amount: float = Field(..., gt=0, description="The initial investment amount. Must be greater than zero.")
    annual_rate: float = Field(..., gt=0.0, lt=1.0, description="The annual interest rate, expressed as a decimal (e.g., 0.05 for 5%). Must be strictly between 0 and 1.")
    periods: int = Field(..., gt=0, lt=30, description="The number of compounding periods (years). Must be a positive integer less than 30.")

@tool(args_schema=InvestmentParameters)
def calculate_time_value(principal_amount: float, annual_rate: float, periods: int) -> str:
    """
    Calculates the future value of an investment using compound interest (FV = P * (1 + r)^n). 
    Requires principal (>0), an annual rate (decimal 0.0 to 1.0), and periods (>0, <30).
    The annual rate MUST be input as a decimal (e.g., 0.05, not 5).
    """
    
    # Pydantic validation ensures inputs are safe before this line executes.
    try:
        future_value = principal_amount * ((1 + annual_rate) ** periods)
        return (f"The principal of ${principal_amount:,.2f} compounded at {annual_rate*100:.2f}% "
                f"over {periods} periods results in a future value of ${future_value:,.2f}.")
    except Exception as e:
        # Fallback for unexpected runtime errors
        return f"An unexpected calculation error occurred: {e}"

# Example of how validation failure is handled (for demonstration only)
def test_validation_failure_demonstration():
    """Simulates a failed Pydantic validation attempt."""
    print("\n--- Pydantic Validation Failure Test (Demonstration) ---")
    try:
        # Attempt to create an invalid model instance (negative principal, rate too high, periods too high)
        InvestmentParameters(principal_amount=-100.0, annual_rate=1.5, periods=50)
    except ValidationError as e:
        # The agent executor captures this structure and returns it to the LLM
        error_details = e.errors()
        print("Validation failed:")
        for error in error_details:
            print(f"  Field: {error['loc'][0]}, Error Type: {error['type']}, Message: {error['msg']}")

# --- Exercise 3: Asynchronous Log Aggregation Tool ---

class LogQuery(BaseModel):
    """Schema for querying system logs."""
    service_name: str = Field(..., description="The name of the microservice whose logs are required.")

@tool(args_schema=LogQuery)
async def aggregate_system_logs(service_name: str) -> str:
    """
    Asynchronously queries the distributed log aggregator for detailed system logs. 
    
    CRITICAL NOTE: This operation simulates a slow, I/O-bound network call and 
    takes approximately 2 seconds to complete. Use this tool for background or 
    non-immediate log analysis tasks where waiting is acceptable.
    """
    # Simulate I/O bound operation
    await asyncio.sleep(2.0) 
    
    if "critical" in service_name.lower():
        return f"Aggregated 1,200 lines of critical logs for {service_name}. Two major errors detected."
    else:
        return f"Successfully aggregated logs for {service_name}. Status: OK."

# --- Exercise 4: Interactive Challenge: Integrating the Inventory Management System ---

class ProductQuery(BaseModel):
    """Schema for checking product stock levels."""
    product_sku: str = Field(..., description="The unique stock keeping unit (SKU) of the product.")
    warehouse_id: str = Field("main", description="Optional ID of the warehouse to check. Defaults to 'main'.")

@tool(args_schema=ProductQuery)
def check_inventory(product_sku: str, warehouse_id: str = "main") -> str:
    """
    CRITICAL INVENTORY MANAGEMENT TOOL: Checks the real-time stock level for a specific product 
    using its SKU in the specified warehouse. Use this tool ONLY for questions regarding 
    current stock, availability, or fulfillment capability. Do not use for general web searches.
    """
    if product_sku == "PROD-404":
        return f"Product {product_sku} is currently OUT OF STOCK in warehouse {warehouse_id}. No fulfillment possible."
    elif product_sku.startswith("PROD"):
        # Simulate varying stock levels
        stock = hash(product_sku) % 100 + 5
        return f"Product {product_sku} has {stock} units available in warehouse {warehouse_id}."
    else:
        return f"Error: Invalid SKU format provided: {product_sku}. Check inventory requires a valid SKU starting with 'PROD'."

# Simulated existing tools for integration context
@tool
def search_web(query: str) -> str:
    """A generic tool for searching external web sources for general knowledge or current events."""
    return f"Search results for '{query}': Found 3 relevant external articles."

@tool
def check_shipping_status(order_id: str) -> str:
    """Synchronously checks the delivery status of a customer order using the order ID."""
    return f"Order {order_id} is currently in transit."

# Integration Simulation: Packaging the tools for the AgentExecutor
inventory_tools = [
    search_web, 
    check_shipping_status, 
    check_inventory 
]

# Testing Simulation: LLM Thought Process
"""
Prompt: "Do we have PROD-404 in stock?"

LLM Thought Process Simulation:
1. Goal: Determine the availability (stock level) of product PROD-404.
2. Tool Analysis based on Descriptions:
    - search_web: Too general; handles external knowledge, not internal inventory.
    - check_shipping_status: Irrelevant; handles order tracking, not stock.
    - check_inventory: Highly specific. The description explicitly labels it the 'CRITICAL INVENTORY MANAGEMENT TOOL' and states it is for 'current stock, availability, or fulfillment capability'.
3. Action Selection: check_inventory.
4. Input Formatting: The required input is product_sku.
Action: check_inventory(product_sku='PROD-404')
"""

# --- Exercise 5: Tool Conflict Resolution and Specificity ---

class UserProfileQuery(BaseModel):
    """Input schema for querying internal user profiles."""
    user_id: int = Field(..., description="The internal proprietary user ID number (integer).")

@tool(args_schema=UserProfileQuery)
def get_user_profile(user_id: int) -> str:
    """
    INTERNAL DATA RETRIEVAL: Use this tool ONLY for querying proprietary internal system 
    user profiles based on their unique integer user_id. This tool cannot access external URLs.
    """
    return f"Retrieved internal user profile data for ID {user_id}: Status Active, Role Admin."

class ExternalDataQuery(BaseModel):
    """Input schema for fetching data from external web endpoints."""
    endpoint_url: str = Field(..., description="The full HTTP/S URL of the external API endpoint to query.")

@tool(args_schema=ExternalDataQuery)
def fetch_external_data(endpoint_url: str) -> str:
    """
    EXTERNAL DATA RETRIEVAL: Use this tool ONLY for making general GET requests 
    to external web resources and public APIs. Requires a full URL (e.g., https://api.example.com). 
    Do NOT use this for internal user IDs or proprietary systems.
    """
    if "example.com" in endpoint_url:
        return f"Successfully fetched external data from {endpoint_url}. Latest news: Market up 2%."
    return f"Fetched generic external data from {endpoint_url}."

# Integration and Conflict Test:
conflict_tools = [
    get_user_profile,
    fetch_external_data
]

# Refinement and Conflict Test Simulation:
"""
Prompt: "I need the profile details for user 1024. Also, what is the latest news from https://www.example.com?"

LLM Thought Process Simulation for Conflict Resolution:
1. Deconstruct Request:
    - Part 1: "profile details for user 1024" (Requires an internal ID, 1024 is an integer).
    - Part 2: "latest news from https://www.example.com" (Requires an external URL).
2. Tool Selection for Part 1 (User ID):
    - get_user_profile: Description specifies 'ONLY for querying proprietary internal system user profiles based on their unique integer user_id.' -> Perfect match.
    - fetch_external_data: Description specifies 'Do NOT use this for internal user IDs.' -> Excluded.
3. Tool Selection for Part 2 (External URL):
    - fetch_external_data: Description specifies 'ONLY for making general GET requests... Requires a full URL.' -> Perfect match.
    - get_user_profile: Description specifies 'This tool cannot access external URLs.' -> Excluded.
4. Conclusion: The specific descriptions successfully guide the LLM to use get_user_profile for the ID and fetch_external_data for the URL, resolving the potential conflict.
"""

if __name__ == '__main__':
    # --- Local Testing Block ---
    
    print("--- Exercise 1 Results ---")
    print(read_config_key("database_url"))
    print(read_config_key("secret_key"))
    
    print("\n--- Exercise 2 Results ---")
    # Successful calculation
    print(calculate_time_value(principal_amount=5000.0, annual_rate=0.07, periods=5))
    # Demonstration of constraint failure (Pydantic intercepts this)
    test_validation_failure_demonstration() 

    print("\n--- Exercise 3 Results ---")
    # Note: To run the async tool, you need an async loop.
    # For demonstration purposes, we show how to call it if a runtime is available.
    if asyncio.get_event_loop().is_running():
        print("Async tool defined successfully. Requires AgentExecutor for runtime testing.")
    else:
        print(asyncio.run(aggregate_system_logs(service_name="payment_gateway")))
        
    print("\n--- Exercise 4 Results ---")
    print(check_inventory(product_sku="PROD-404"))
    print(check_inventory(product_sku="PROD-100", warehouse_id="west"))
