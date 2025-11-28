
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
from datetime import datetime
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- 0. Environment Setup and LLM Initialization ---

# NOTE: Assumes OPENAI_API_KEY is set in the environment variables.
# For local testing, ensure the key is available.
try:
    llm = OpenAI(temperature=0)
except Exception as e:
    print(f"Error initializing LLM. Ensure API key is set: {e}")
    exit()

# --- 1. Defining Custom Tools (The Agent's Capabilities) ---

def get_current_datetime(input_text: str) -> str:
    """
    Utility function that returns the current date and time.
    The input_text parameter is required by the Tool interface but ignored here.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Wrap the function into a LangChain Tool object
date_tool = Tool(
    name="Current Date/Time Getter",
    func=get_current_datetime,
    description="Useful for answering questions about the current date and time, especially for time-sensitive queries."
)

# --- 2. Loading Standard Tools ---

# The 'llm-math' tool is a standard utility that encapsulates a calculation
# chain, allowing the Agent to perform precise arithmetic operations.
math_tools = load_tools(["llm-math"], llm=llm)

# --- 3. Combining Tools and Initializing the Agent Executor ---

# Combine all available tools into a single list
all_tools = math_tools + [date_tool]

# Initialize the Agent Executor
# AgentType.ZERO_SHOT_REACT_DESCRIPTION is the core ReAct implementation.
# 'Zero Shot' means the LLM is given the tool descriptions and relies solely
# on its general knowledge (zero examples) to decide the next step.
agent = initialize_agent(
    tools=all_tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True, # CRITICAL: This enables the visualization of the ReAct loop
    handle_parsing_errors=True # Robustness feature
)

# --- 4. Executing the Multi-Step Prompt ---

prompt = "I need two pieces of information: First, what is 387 divided by 12? Second, what is the exact time right now?"

print("\n" + "="*50)
print(f"Executing Prompt: {prompt}")
print("="*50 + "\n")

# The agent.run() method initiates the iterative Thought/Action/Observation process
response = agent.run(prompt)

print("\n" + "="*50)
print("--- Agent Execution Complete ---")
print(f"Final Answer: {response}")
print("="*50)
