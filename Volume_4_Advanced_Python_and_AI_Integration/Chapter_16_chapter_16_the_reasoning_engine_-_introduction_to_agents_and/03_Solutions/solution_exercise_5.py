
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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

# 1. Faulty Tool Simulation
class FaultyConverterTool:
    name = "Faulty_Converter"
    description = "Converts numbers to other formats, but requires the input to be 'safe' for security reasons."

    def convert(self, input_str: str) -> str:
        """Raises ValueError if the input doesn't contain the safety keyword."""
        if "safe" not in input_str.lower():
            raise ValueError("Input validation failed: Missing required safety keyword.")
        
        # Mock successful conversion if 'safe' is present
        return f"Successfully converted '{input_str}' to Roman numeral: V"

# 2. Execution Wrapper for Error Handling
def execute_tool_with_error_handling(tool_instance: Any, action_input: str) -> str:
    """
    Simulates the agent executor catching a tool error and formatting the observation.
    """
    try:
        # Assuming the tool has a primary method named 'convert'
        result = tool_instance.convert(action_input)
        return f"Observation: {result}"
    except Exception as e:
        # Standardized error message for the LLM to parse
        error_message = f"TOOL ERROR: Input validation failed. Check required parameters. Details: {str(e)}"
        return f"Observation: {error_message}"

# 3. Agent Prompt Modification (Conceptual)
# The system prompt would contain instructions like:
AGENT_SYSTEM_PROMPT = """
If your Observation begins with 'TOOL ERROR:', you MUST generate a 'Self-Correction Thought:' 
explaining the failure and proposing a new, corrected Action before proceeding.
"""

# --- Test Case Simulation ---
faulty_tool = FaultyConverterTool()
calculator_tool = CalculatorTool # Re-use from Ex 4

# Query: "Convert the number 5 to Roman numerals. If that fails, just tell me the result of 5 + 5."

print("--- Step 1: Intentional Failure ---")
llm_turn_1 = "Thought: I must use the Faulty_Converter tool first.\nAction: Faulty_Converter\nAction Input: 5"
print(f"LLM Output:\n{llm_turn_1}")

# Execute the action, triggering the failure
obs_1 = execute_tool_with_error_handling(faulty_tool, "5")
print(f"\nExecutor Response:\n{obs_1}")

# --- Step 2: Self-Correction and Recovery ---
# The LLM receives the Observation: TOOL ERROR... and must self-correct.
llm_turn_2 = f"""
{obs_1}
Self-Correction Thought: The previous action failed because the input '5' did not contain the required safety keyword, as indicated by the TOOL ERROR. I must now pivot to the backup plan: calculating 5 + 5 using the CalculatorTool.
Action: CalculatorTool
Action Input: 5 + 5
"""
print(f"\n--- Step 2: LLM Self-Correction ---")
print(llm_turn_2)

# Execute the corrected action
action_match = re.search(r"Action:\s*(\w+)", llm_turn_2)
input_match = re.search(r"Action Input:\s*(.*)", llm_turn_2, re.DOTALL)
action_name = action_match.group(1).strip()
action_input = input_match.group(1).strip()

obs_2 = calculator_tool(action_input)
print(f"\nExecutor Response (Corrected Action):\nObservation: {obs_2}")

# --- Step 3: Final Answer ---
llm_turn_3 = f"""
Observation: {obs_2}
Thought: The calculation was successful. I have recovered from the initial error and can now provide the final answer based on the successful calculation.
Final Answer: Although the conversion failed, the calculation result of 5 + 5 is 10.
"""
print(f"\n--- Step 3: Final Answer ---")
print(llm_turn_3)
