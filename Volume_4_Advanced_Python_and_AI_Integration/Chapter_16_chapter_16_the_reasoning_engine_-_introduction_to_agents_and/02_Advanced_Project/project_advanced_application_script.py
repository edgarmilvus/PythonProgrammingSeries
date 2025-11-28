
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
from typing import Dict, Any
from langchain.agents import initialize_agent, AgentType, Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.pydantic_v1 import BaseModel, Field

# --- 1. Environment Setup and LLM Initialization ---
# NOTE: Replace 'your_api_key' with os.environ.get("OPENAI_API_KEY") in production
# Assuming OPENAI_API_KEY is set in the environment for simplicity.
if not os.environ.get("OPENAI_API_KEY"):
    print("WARNING: OPENAI_API_KEY environment variable not set. Using dummy key.")
    # This is required for initialization, even if using mocks.
    os.environ["OPENAI_API_KEY"] = "DUMMY_KEY_FOR_DEMO" 

# Initialize the foundational LLM for the agent's reasoning (Thought/Planning)
# Using a powerful model suitable for complex reasoning tasks.
llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")

# --- 2. Custom Tool Definitions (The 'Action' Component) ---

# Define the input schema for type safety and clarity for the LLM
class StockInput(BaseModel):
    """Input structure for the Stock Price Lookup Tool."""
    symbol: str = Field(description="The ticker symbol of the stock (e.g., GOOGL).")

def get_stock_price(symbol: str) -> str:
    """
    Simulates fetching the current market price for a given stock symbol.
    In a real application, this would call a financial API (e.g., Alpha Vantage).
    """
    symbol = symbol.upper()
    
    # Mock data based on symbol
    if symbol == "GOOGL":
        price = 175.50
    elif symbol == "TSLA":
        price = 185.00
    else:
        return f"Error: Stock symbol {symbol} not found in mock database."
        
    return f"The current price for {symbol} is ${price:.2f}."

# Define the input schema for the Risk Assessment Tool
class RiskAssessmentInput(BaseModel):
    """Input structure for the Proprietary Risk Assessment Tool."""
    price: float = Field(description="The current market price of the stock.")
    symbol: str = Field(description="The ticker symbol of the stock being analyzed.")

def proprietary_risk_assessment(price: float, symbol: str) -> str:
    """
    Applies a proprietary, multi-condition rule set to the stock price.
    This simulates complex business logic that the LLM cannot execute internally.
    """
    symbol = symbol.upper()
    
    if symbol == "GOOGL":
        # Rule 1: Threshold check (below $180 is attractive)
        if price < 180.00:
            # Rule 2: Volatility check (simulated)
            if price < 170.00:
                return f"GOOGL price (${price:.2f}) is significantly below the $180 threshold. Recommendation: STRONG BUY."
            else:
                return f"GOOGL price (${price:.2f}) is below the $180 threshold. Recommendation: BUY."
        # Rule 3: Overvalued check
        elif price > 190.00:
            return f"GOOGL price (${price:.2f}) is above the $190 risk ceiling. Recommendation: SELL/HOLD."
        else:
            return f"GOOGL price (${price:.2f}) is within the neutral range ($180-$190). Recommendation: HOLD."
    
    # Fallback for other symbols
    return f"Risk assessment logic not defined for {symbol}. Price: ${price:.2f}. Recommendation: NEUTRAL."


# Package the custom functions into LangChain Tool objects
tools = [
    Tool(
        name="StockPriceTool",
        func=get_stock_price,
        description="A tool for retrieving the current market price of a stock using its ticker symbol.",
        args_schema=StockInput
    ),
    Tool(
        name="ProprietaryRiskAssessmentTool",
        func=proprietary_risk_assessment,
        description="A proprietary tool that applies complex business logic to a stock's price to generate an investment recommendation (BUY/HOLD/SELL). Requires price and symbol.",
        args_schema=RiskAssessmentInput
    )
]

# --- 3. Agent Initialization and Execution ---

# Initialize the Agent using the ReAct framework (ZERO_SHOT_REACT_DESCRIPTION)
# This type forces the LLM to generate a Thought before every Action.
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True, # Critical for seeing the Thought/Action/Observation loop
    handle_parsing_errors=True
)

# Define the complex, multi-step task for the agent
task_prompt = "Using the provided tools, analyze GOOGL stock. First, get its current price. Second, apply the proprietary risk assessment to the price found. Finally, summarize the resulting recommendation clearly."

print("\n" + "="*80)
print(f"Executing Agent Task: {task_prompt}")
print("="*80)

# Run the agent
try:
    result = agent.run(task_prompt)
    print("\nAGENT FINAL RESULT:")
    print(result)
    print("="*80)

except Exception as e:
    print(f"\nAn error occurred during agent execution: {e}")

