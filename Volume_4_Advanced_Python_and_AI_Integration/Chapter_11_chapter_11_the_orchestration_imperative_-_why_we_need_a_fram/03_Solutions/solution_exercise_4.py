
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

# 1. Define External Data
INVENTORY_DB = {
    "P001": 550,
    "P002": 12,
    "P003": 980
}

# 2. Create a Custom Tool
def get_inventory_stock(product_id: str) -> str:
    """Accepts a product ID (e.g., 'P001') and returns the current stock level as an integer string. Returns '0' if not found."""
    stock = INVENTORY_DB.get(product_id.upper(), 0)
    return str(stock)

inventory_tool = Tool.from_function(
    func=get_inventory_stock,
    name="InventoryLookup",
    description="Useful for finding the current stock level of a specific product ID. Input must be the product ID string."
)

def exercise_3_tools(llm: ChatOpenAI):
    """
    Sets up an Agent with a custom tool for RAG simulation.
    """
    if not llm:
        print("LLM not initialized. Skipping Exercise 3.")
        return

    print("\n--- EXERCISE 3: RAG Simulation with Tools ---")
    
    tools = [inventory_tool]
    
    # 3. Agent Setup
    # Using ZERO_SHOT_REACT_DESCRIPTION to force the Agent to use the Thought/Action/Observation cycle
    agent_executor = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True, # Critical for validation
        handle_parsing_errors=True
    )
    
    # 5. Execution
    prompt = "I need to know the current stock level for product ID 'P001' and then summarize the importance of maintaining high stock for this key item."
    print(f"\n[Agent Prompt]: {prompt}")
    
    try:
        agent_executor.invoke({"input": prompt})
    except Exception as e:
        # Agents can sometimes fail due to LLM reasoning errors, 
        # but the verbose output should still show the successful tool call.
        print(f"\nAgent execution finished (potential final parsing error): {e}")

# exercise_3_tools(llm)
