
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

from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- 1. Tool Definition ---

# Tool 1 Schema & Function (Data Retrieval)
class StockPriceInput(BaseModel):
    """Input schema for getting a stock's current price."""
    ticker: str = Field(description="The stock ticker symbol (e.g., MSFT, AAPL).")

@tool(args_schema=StockPriceInput)
def get_current_stock_price(ticker: str) -> float:
    """Retrieves the current market price for a given stock ticker."""
    if ticker.upper() == "MSFT":
        return 420.00  # Simulated current price
    else:
        return 100.00

# Tool 2 Schema & Function (Computation)
class ProfitLossInput(BaseModel):
    """Input schema for projecting profit or loss."""
    initial_price: float = Field(description="The purchase price of the shares.")
    target_price: float = Field(description="The expected selling price of the shares.")
    shares: int = Field(description="The total number of shares involved.")

@tool(args_schema=ProfitLossInput)
def project_profit_loss(initial_price: float, target_price: float, shares: int) -> str:
    """
    Calculates the total potential profit or loss based on initial price,
    target price, and the number of shares.
    """
    profit_per_share = target_price - initial_price
    total_profit_loss = profit_per_share * shares
    
    if total_profit_loss >= 0:
        return f"Projected Profit: ${total_profit_loss:,.2f}"
    else:
        return f"Projected Loss: ${abs(total_profit_loss):,.2f}"

# --- 2. Agent Initialization ---
llm_financial = ChatOpenAI(temperature=0, model="gpt-4o") # Use a capable model for complex reasoning

tools_financial = [get_current_stock_price, project_profit_loss]

prompt_financial = ChatPromptTemplate.from_messages([
    ("system", "You are a sophisticated Financial Decision Agent. You must break down complex requests into sequential tool calls. Always use the output of the first tool as input for the second tool when necessary."),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent_financial = create_openai_tools_agent(llm_financial, tools_financial, prompt_financial)
agent_executor_financial = AgentExecutor(
    agent=agent_financial, 
    tools=tools_financial, 
    verbose=True, # Enable verification of steps
    handle_parsing_errors=True
)

# --- 3 & 4. Complex Query Execution and Verification ---
complex_query = "If I buy 100 shares of MSFT right now, and the price hits $450, how much profit would I make?"

print(f"--- Executing Complex Query: {complex_query} ---")
result = agent_executor_financial.invoke({"input": complex_query})
print("\n--- Final Result ---")
print(result['output'])
# Expected steps in verbose output:
# 1. Calls get_current_stock_price('MSFT') -> 420.00
# 2. Calls project_profit_loss(initial_price=420.00, target_price=450.00, shares=100) -> $3,000.00
