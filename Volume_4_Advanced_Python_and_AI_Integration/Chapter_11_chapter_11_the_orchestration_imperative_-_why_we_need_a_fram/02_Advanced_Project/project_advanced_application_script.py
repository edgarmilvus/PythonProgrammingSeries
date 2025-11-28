
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
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_core.messages import SystemMessage

# --- 1. Environment and Mock Data Setup ---
# NOTE: Replace 'os.environ["OPENAI_API_KEY"]' with a MockLLM or your actual key
# For production, always use environment variables.
try:
    # Attempt to use a real key if available, otherwise mock the environment
    _ = os.environ["OPENAI_API_KEY"]
except KeyError:
    print("WARNING: OPENAI_API_KEY not set. Using a placeholder for demonstration.")
    # In a real scenario, we would use a MockLLM. For this example, we assume the environment is set up.
    # We will proceed assuming the necessary environment is configured for execution.
    pass

# Simulated external data source (e.g., a database or vector store payload)
MOCK_FINANCIAL_DATA: Dict[str, Dict[str, Any]] = {
    "TSLA": {"price": 185.50, "market_cap": "580B", "sentiment": "Mixed, due to recent acquisition news."},
    "GOOGL": {"price": 170.15, "market_cap": "2.1T", "sentiment": "Strong, driven by AI product launches."},
    "NVDA": {"price": 950.00, "market_cap": "2.3T", "sentiment": "Extremely bullish, dominating the AI hardware market."}
}

# --- 2. Define the External Tool (Simulating RAG/Database Lookup) ---

def get_financial_data(ticker_symbol: str) -> str:
    """
    Retrieves detailed financial data for a given stock ticker.
    This simulates a call to an external API or a RAG system.
    """
    ticker = ticker_symbol.upper().strip()
    data = MOCK_FINANCIAL_DATA.get(ticker)
    
    if data:
        # Format the structured data into a digestible string for the LLM
        return f"Financial Data for {ticker}: Price: {data['price']}, Market Cap: {data['market_cap']}, Analyst Sentiment: {data['sentiment']}"
    else:
        return f"Error: No financial data found for ticker {ticker}. Please try TSLA, GOOGL, or NVDA."

# Create the LangChain Tool object
financial_tool = Tool(
    name="FinancialDataRetriever",
    func=get_financial_data,
    description="Useful for retrieving real-time stock prices, market capitalization, and analyst sentiment for specific stock tickers (e.g., TSLA, GOOGL)."
)

# --- 3. Initialize Core Orchestration Components ---

# A. The LLM (The Brain)
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini") 

# B. The Memory (The State Manager)
# This component tracks the conversation history and injects it into the prompt.
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# C. The Toolset (The External Knowledge)
tools = [financial_tool]

# D. System Prompt (The Personality and Context)
system_message = SystemMessage(
    content=(
        "You are a sophisticated Financial Analyst AI. Your goal is to provide concise, data-driven "
        "insights based on the information provided by your tools or your memory. "
        "Always use the 'FinancialDataRetriever' tool when asked about specific stock metrics. "
        "Maintain a professional and helpful tone."
    )
)

# --- 4. Construct the Agent Executor (The Orchestrator) ---

# The Agent Executor binds the LLM, the tools, and the memory together.
# AgentType.OPENAI_FUNCTIONS is highly effective for tool selection.
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True, # Critical for seeing the orchestration steps
    memory=memory,
    handle_parsing_errors=True,
    agent_kwargs={"system_message": system_message}
)

# --- 5. Execute Multi-Step Reasoning and State Management ---

print("--- QUERY 1: Tool Use and Initial Context Setting ---")
query_1 = "What is the current market sentiment and price for NVDA? Please summarize the data."

# The agent must decide to use the tool, execute it, and then synthesize the result.
response_1 = agent_executor.invoke({"input": query_1})
print(f"\n[AGENT RESPONSE 1]:\n{response_1['output']}\n")

print("--- QUERY 2: Memory and Context Retrieval Test ---")
# This query relies on the memory of the first query ("NVDA") and general knowledge.
query_2 = "Based on that stock, what is a major competitor in the AI chip sector?"

# The agent must recognize 'that stock' refers to NVDA (from memory) and then answer
# using general LLM knowledge, without needing the tool again.
response_2 = agent_executor.invoke({"input": query_2})
print(f"\n[AGENT RESPONSE 2]:\n{response_2['output']}\n")

# --- 6. Inspection of Memory State ---
print("\n--- FINAL MEMORY STATE INSPECTION ---")
print(memory.load_memory_variables({}))

