
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
import json
import asyncio
import re
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# --- Prerequisites and Setup ---
# Ensure the API key is set in your environment variables
if "GEMINI_API_KEY" not in os.environ:
    # Note: In a real environment, this error should be raised. 
    # For execution robustness in a controlled environment, we check existence.
    if not os.getenv("GEMINI_API_KEY"):
        print("Warning: GEMINI_API_KEY environment variable not set. Client initialization might fail.")

# Initialize the client
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    # Exit if client cannot be initialized due to missing key or other error
    # exit() 
    pass # Allow code to run for structural demonstration if key is missing

# --- Exercise 3 Setup: Custom Tool Schema (Function Calling) ---
class InventoryCheck(BaseModel):
    """Schema for checking the inventory status of a specific product."""
    product_id: str = Field(description="The unique identifier for the product (e.g., P-401).")
    required_quantity: int = Field(description="The quantity the user needs to order or check against.")

def get_warehouse_inventory(product_id: str, required_quantity: int) -> dict:
    """
    Retrieves the current stock level for a product.
    NOTE: This function is defined here but will NOT be executed in Exercise 3.
    We are only demonstrating the schema declaration and the model's decision to call it.
    """
    # In a real application, this would call a database or external service
    return {
        "tool_name": "get_warehouse_inventory",
        "product_id": product_id,
        "required_quantity": required_quantity,
        "status": "Success",
        "current_stock": 850
    }

# Convert the Python function definition into a Gemini tool declaration
INVENTORY_TOOL = types.Tool.from_callable(get_warehouse_inventory)


async def run_exercises():
    """Runs Exercises 1, 2, 3, and 4."""
    
    # --- Exercise 1: Real-Time Fact Checker (Google Search) ---
    print("\n" + "="*50)
    print("--- Exercise 1: Google Search Grounding ---")
    print("="*50)
    recent_event_prompt = "Who won the latest major international chess tournament and what was the prize fund?"
    
    try:
        response_e1 = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=recent_event_prompt,
            tools=[types.Tool.google_search()] # Enable Google Search
        )
        print(f"Prompt: {recent_event_prompt}")
        print(f"Response Text: {response_e1.text[:200]}...")
        
        # Analyze the Response for grounding metadata
        grounding_data = response_e1.candidates[0].grounding_metadata
        if grounding_data and grounding_data.web_search_queries:
            print(f"\n[Verification]")
            print(f"SUCCESS: Grounding data found. Tool Activated.")
            print(f"Search Queries Used: {grounding_data.web_search_queries}")
        else:
            print("[Verification]")
            print("INFO: No grounding data found, or tool was not necessary for the answer.")
            
    except Exception as e:
        print(f"Error in Exercise 1: {e}")


    # --- Exercise 2: Chained Built-in Tools (Search + Code Execution) ---
    print("\n" + "="*50)
    print("--- Exercise 2: Search and Code Execution ---")
    print("="*50)
    complex_query = "Find the current market capitalization of the largest company based in Seoul, South Korea, and then calculate exactly 2.3% of that total value."
    
    try:
        response_e2 = client.models.generate_content(
            model='gemini-2.5-pro', # Pro model often better at complex tool chaining
            contents=complex_query,
            tools=[
                types.Tool.google_search(),
                types.Tool.code_execution()
            ]
        )
        print(f"Prompt: {complex_query}")
        print(f"Response Text: {response_e2.text[:300]}...")
        print("\n[Verification]")
        print("Model successfully combined real-time data retrieval (Search) with precise calculation (Code Execution).")
        # Note: We rely on the accuracy of the final answer to confirm tool chain success.

    except Exception as e:
        print(f"Error in Exercise 2: {e}")


    # --- Exercise 3: Custom Tool Declaration (Function Calling Setup) ---
    print("\n" + "="*50)
    print("--- Exercise 3: Function Calling Detection (Planning Phase) ---")
    print("="*50)
    inventory_prompt = "I need to check the stock for product P-401. Do we have enough inventory to cover a large order of 500 units?"
    
    try:
        response_e3 = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=inventory_prompt,
            tools=[INVENTORY_TOOL]
        )
        print(f"Prompt: {inventory_prompt}")
        
        # Check if the model decided to call the function
        if response_e3.function_calls:
            print("\n[Verification]")
            print("SUCCESS: Model requested a function call (Planning complete).")
            
            # Extract the structured call
            call = response_e3.function_calls[0]
            print(f"Function Requested: {call.name}")
            print(f"Arguments Provided (JSON): {dict(call.args)}")
            
        else:
            print("[Verification]")
            print("FAILURE: Model responded with text instead of a function call.")

    except Exception as e:
        print(f"Error in Exercise 3: {e}")


    # --- Exercise 4: Dynamic URL Context Integration ---
    print("\n" + "="*50)
    print("--- Exercise 4: Dynamic URL Context Activation ---")
    print("="*50)
    
    # Simple regex to detect a URL
    url_pattern = re.compile(r'https?://[^\s]+')

    async def async_chat_session(prompt: str):
        """Simulates a single turn in a chat session with dynamic tool activation."""
        print(f"Input Prompt: '{prompt[:50]}...'")
        
        # 1. Check for URL presence
        urls_found = url_pattern.findall(prompt)
        
        # 2. Conditional Tool Activation
        active_tools = []
        if urls_found:
            # The URL Context tool requires the URL to be passed in the contents/prompt
            active_tools.append(types.Tool.url_context())
            print(f"-> URL detected: Activating URL Context tool for this turn.")
        else:
            print("-> No URL detected: Proceeding without URL Context.")

        # 3. Execute the call
        response = await client.models.generate_content_async(
            model='gemini-2.5-flash',
            contents=prompt,
            tools=active_tools if active_tools else None
        )
        
        print(f"Response (First 100 chars): {response.text[:100]}...")
        
        # Verification check
        grounding_data = response.candidates[0].grounding_metadata
        if active_tools and grounding_data and grounding_data.uri_context:
            print("-> Verification: URI Context metadata confirms tool use.")
        elif not active_tools and not grounding_data:
            print("-> Verification: Standard response, no tool metadata present.")
        
        print("-" * 20)

    # Test Case A: URL present
    await async_chat_session("Please analyze the key takeaways from the article found at https://ai.google.dev/gemini-api/docs/tools")
    
    # Test Case B: Standard query (no URL)
    await async_chat_session("What are the three core principles of object-oriented programming?")


# --- Exercise 5: Architectural Challenge (Simulating Agent Parallelism) ---

async def async_tool_A(arg: str):
    """Simulates a slow tool call (e.g., calling an external weather API)."""
    print(f"  [Tool A] Starting execution with arg: {arg}")
    await asyncio.sleep(1.5)
    result = {"tool_A_result": f"Data for {arg} processed successfully."}
    print("  [Tool A] Finished.")
    return result

async def async_tool_B(arg1: int, arg2: float):
    """Simulates another slow tool call (e.g., calculating complex logistics)."""
    print(f"  [Tool B] Starting execution with args: {arg1}, {arg2}")
    await asyncio.sleep(0.5)
    calc = arg1 * arg2
    result = {"tool_B_result": f"Calculation complete: {calc}"}
    print("  [Tool B] Finished.")
    return result

async def execute_tool_calls_in_parallel(function_calls_from_gemini: list):
    """
    Simulates the agent's execution phase using asyncio.TaskGroup 
    to handle multiple tool requests concurrently.
    """
    print("\n" + "="*50)
    print("--- Exercise 5: Agent Parallel Execution Simulation ---")
    print("="*50)
    print(f"Agent received {len(function_calls_from_gemini)} tool requests from Gemini.")
    
    tool_map = {
        "tool_a": async_tool_A,
        "tool_b": async_tool_B
    }
    
    all_results = {}
    
    # Use TaskGroup for structured concurrency (Python 3.11+)
    try:
        async with asyncio.TaskGroup() as tg:
            tasks = []
            for call in function_calls_from_gemini:
                tool_name = call['name']
                tool_args = call['args']
                
                if tool_name in tool_map:
                    print(f"Scheduling tool '{tool_name}' for concurrent execution...")
                    # Create a task for the function call using unpacked arguments
                    task = tg.create_task(tool_map[tool_name](**tool_args))
                    tasks.append(task)
                else:
                    print(f"Warning: Tool '{tool_name}' not found in tool map.")
        
        # After the TaskGroup block, all tasks are guaranteed to be complete
        print("\nAll tasks in TaskGroup completed. Collecting results...")
        
        # Collect results and aggregate them using dict.update()
        for task in tasks:
            # The result of the task is the dictionary returned by the async tool function
            all_results.update(task.result())
            
        print("\n[Verification] Consolidated Results for Submission back to Gemini:")
        print(json.dumps(all_results, indent=2))
        
        return all_results
    
    except Exception as e:
        print(f"An error occurred during parallel execution: {e}")
        return {}


# Simulated output from Gemini after processing a prompt (Step 2 of Custom Tool Flow)
simulated_gemini_calls = [
    {"name": "tool_a", "args": {"arg": "San Francisco"}},
    {"name": "tool_b", "args": {"arg1": 1500, "arg2": 0.05}}
]

async def main():
    """Main function to run all exercises asynchronously."""
    await run_exercises()
    
    # Run Exercise 5 simulation
    await execute_tool_calls_in_parallel(simulated_gemini_calls)

if __name__ == "__main__":
    # Note: Running the async main function
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred in the main execution loop: {e}")
