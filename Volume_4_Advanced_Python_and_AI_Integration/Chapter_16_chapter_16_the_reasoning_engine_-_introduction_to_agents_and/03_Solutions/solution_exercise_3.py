
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

# Source File: solution_exercise_3.py
# Description: Solution for Exercise 3
# ==========================================

import textwrap

# 1. Verbose Tool Definition
def VerboseAPITool(query: str) -> str:
    """
    Mock API tool that returns a noisy, multi-paragraph observation.
    The critical data is hidden within.
    """
    return textwrap.dedent(f"""
        --- API RESPONSE START ---
        Query Processed: {query}
        [LOG] Request ID: ABC-12345. Time taken: 450ms. Status: 200 OK.
        
        The primary analysis shows market volatility is high, affecting non-essential goods.
        Detailed breakdown of Q3 revenue projections is attached in Appendix A (omitted here).
        
        CRITICAL DATA POINT: The required security token for the next step is 'TOKEN_X7Y9Z'.
        
        Further notes on compliance: All transactions must adhere to ISO 27001 standards.
        The system will automatically log out inactive users after 60 minutes.
        --- API RESPONSE END ---
    """)

# 2. Refinement LLM Simulation
REFINEMENT_PROMPT = textwrap.dedent("""
    You are a Data Filter. Your task is to extract the single, critical piece of data
    required for the agent's next action from the following raw observation.
    Output ONLY the extracted data, nothing else.

    Critical Data Target: Security Token
    Raw Observation:
    ---
    {raw_observation}
    ---
    Refined Data:
""")

def refine_observation(raw_observation: str, refinement_prompt: str) -> str:
    """
    Simulates sending the raw observation through a separate LLM chain for refinement.
    
    Note: In a real scenario, this function would call the LLM API.
    Here, we simulate the LLM's ability to extract the token based on the prompt.
    """
    # Simple simulation of LLM extraction based on the target
    if "CRITICAL DATA POINT: The required security token" in raw_observation:
        # Mocking the LLM successfully extracting the key phrase
        return "TOKEN_X7Y9Z"
    return "Error: Could not extract critical data."

# 3. Agent Execution Flow Simulation
initial_query = "Retrieve the security token required to access the next stage."

# Step 1: Agent calls the verbose tool
print(f"Agent Action: Call VerboseAPITool with input: {initial_query}")
raw_observation = VerboseAPITool(initial_query)
print(f"\n--- Raw Observation Received (Length: {len(raw_observation)} chars) ---")
# print(raw_observation) # Too verbose to print fully

# Step 2: Agent triggers the Refinement Step
print("\n--- Agent Thought: Raw observation is too verbose. Initiating Refinement LLM ---")
refined_data = refine_observation(raw_observation, REFINEMENT_PROMPT)

# Step 3: Append the Refined Observation back to the scratchpad
refined_observation_text = f"Refined Observation: The required security token is {refined_data}"
print(f"\n{refined_observation_text}")

# Step 4: Agent continues the ReAct loop using the refined data
llm_next_thought = f"Thought: I have successfully filtered the observation and retrieved the token. I can now proceed to the final answer."
final_answer = f"Final Answer: The security token needed is {refined_data}."

print(f"\n{llm_next_thought}")
print(final_answer)
