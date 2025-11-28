
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
import tempfile
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.agents.agent_toolkits import create_retriever_tool

# --- 1. Configuration and Setup ---
# NOTE: Replace 'gpt-3.5-turbo' with your preferred model.
# Assumes OPENAI_API_KEY is set in environment variables.
LLM = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")

# --- 2. Custom Tool Definition (Simulating a Real-time API) ---

# Define a function to simulate fetching real-time stock data.
@tool("Stock_Price_Lookup", return_direct=False)
def get_current_stock_price(ticker: str) -> float:
    """
    Looks up the current market price for a given stock ticker.
    Use this tool when current pricing data is required for calculation.
    """
    if ticker.upper() == "FTCH":
        # Mock current price data
        return 150.00
    return 10.00

# --- 3. Retrieval-Augmented Generation (RAG) Setup ---

# Create a temporary document simulating internal policy data
policy_content = (
    "The FinTech Corp Holdings (FTCH) dividend policy mandates an annual payout "
    "of $6.00 per share, distributed quarterly. This policy is reviewed annually "
    "but remains fixed for the current fiscal year 2024."
)
temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt")
temp_file.write(policy_content)
temp_file.close()

# Load, split, and embed the document
loader = TextLoader(temp_file.name)
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Create the vector store and retriever
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)
retriever = vectorstore.as_retriever()

# Wrap the retriever into a LangChain tool
retriever_tool = create_retriever_tool(
    retriever,
    "FTCH_Policy_Retriever",
    "Use this tool to answer questions specifically about the FTCH dividend policy or internal documents."
)

# --- 4. Agent Orchestration ---

# Combine all tools available to the agent
available_tools = [get_current_stock_price, retriever_tool]

# Initialize memory for persistent conversation history
# Memory is crucial for multi-step reasoning (e.g., remembering the dividend amount)
memory = ConversationBufferWindowMemory(
    memory_key="chat_history", 
    k=5, 
    return_messages=True
)

# Initialize the Agent
# We use the 'zero-shot-react-description' type for dynamic tool selection based on reasoning
agent = initialize_agent(
    available_tools,
    LLM,
    agent=AgentType.OPENAI_FUNCTIONS, # Highly effective for tool use
    verbose=True,
    memory=memory,
    handle_parsing_errors=True
)

# --- 5. Execution and Demonstration ---

print("--- Agent Execution: Step 1 (RAG Retrieval) ---")
# Query 1: Forces the agent to use the RAG tool to find the dividend amount.
prompt_1 = "What is the annual dividend payout for FTCH according to the internal documents?"
agent.invoke({"input": prompt_1})

print("\n--- Agent Execution: Step 2 (Synthesis: Memory + Tool + Calculation) ---")
# Query 2: Forces the agent to use the Stock Price Tool, recall the dividend from memory, 
# and perform the final calculation (Yield = Dividend / Price).
prompt_2 = "Given that dividend, what is the effective dividend yield based on the current market price?"
agent.invoke({"input": prompt_2})

# Cleanup the temporary file
os.unlink(temp_file.name)
