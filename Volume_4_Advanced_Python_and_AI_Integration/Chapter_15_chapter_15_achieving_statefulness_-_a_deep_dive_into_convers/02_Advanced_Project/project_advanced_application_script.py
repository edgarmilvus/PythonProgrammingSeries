
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
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.prompts import PromptTemplate

# Load environment variables (API keys)
load_dotenv()

# --- 1. Initialization and Configuration ---

# Ensure the LLM is initialized. We use OpenAI for its robust summarization capabilities.
# NOTE: In a production environment, use environment variables for api_key.
try:
    llm = OpenAI(temperature=0.1, model_name="gpt-3.5-turbo-instruct")
except Exception as e:
    print(f"Error initializing LLM: {e}. Ensure OPENAI_API_KEY is set.")
    exit()

# Define the sequence of user inputs (the conversation history)
CONVERSATION_TURNS = [
    "Hello, I am setting up my finances. I earn $80,000 annually.",
    "My current monthly expenses are $3,500, including rent and utilities.",
    "I am saving up for a down payment on a house, aiming for $50,000 in three years.",
    "I have a high risk tolerance and prefer growth stocks over bonds.",
    "What kind of investment strategy should I pursue given this context?",
    "Also, how much should I allocate monthly to reach that $50k goal?"
]

# --- 2. Memory Setup and Chain Creation ---

# A. Short-Term Memory (Buffer Window) for quick recall demonstration
# We only keep the last 3 exchanges to prevent immediate token bloat
buffer_memory = ConversationBufferWindowMemory(k=3, memory_key="history")

# Chain 1: Used for the initial interactive phase, demonstrating short-term context
buffer_chain = ConversationChain(
    llm=llm,
    memory=buffer_memory,
    verbose=False
)

# B. Long-Term Memory (Summary) for distillation
# This memory will automatically summarize the history using the LLM itself
summary_memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=False # We want a single string summary
)

# Chain 2: Used to build the summary state in the background
summary_chain = ConversationChain(
    llm=llm,
    memory=summary_memory,
    verbose=False
)

# --- 3. Simulating the Conversation and State Update ---

print("--- 3.1: Running Conversation (Updating Buffer and Summary Memories) ---")
for i, user_input in enumerate(CONVERSATION_TURNS):
    print(f"\n[Turn {i+1} User]: {user_input}")
    
    # Run the input through the buffer chain (to update buffer memory state)
    buffer_response = buffer_chain.predict(input=user_input)
    # Run the input through the summary chain (to update summary memory state)
    summary_response = summary_chain.predict(input=user_input)
    
    # We only print the summary chain response for the final turn, 
    # as the buffer chain response is usually immediate and less strategic.
    if i < len(CONVERSATION_TURNS) - 1:
        print(f"[Turn {i+1} Assistant]: ... (Response hidden for brevity)")
    else:
        # For the final turn, print the immediate LLM response to the question
        print(f"[Turn {i+1} Assistant]: {summary_response}")


# --- 4. Inspecting the Memory States ---

print("\n" + "="*50)
print("--- 4.1: Inspection: ConversationBufferWindowMemory (k=3) ---")
# The buffer only holds the last 3 exchanges, demonstrating truncation
print(buffer_memory.load_memory_variables({})['history'])

print("\n" + "="*50)
print("--- 4.2: Inspection: ConversationSummaryMemory (Distilled State) ---")
# The summary memory holds a dense summary of all turns
distilled_context = summary_memory.load_memory_variables({})['chat_history']
print(distilled_context)

# --- 5. Final Strategic Advice Generation (Using Distilled Context) ---

# Define a specialized prompt template that explicitly uses the summary memory key
ADVICE_TEMPLATE = """
You are a Senior Financial Strategist. Your goal is to provide a comprehensive, actionable investment plan.
Use the distilled conversation summary below to tailor your advice.

DISTILLED CONTEXT:
{distilled_context}

INSTRUCTION: Based on the context, provide a detailed 3-part plan:
1. Monthly Allocation Requirement to meet the goal.
2. A specific, high-risk investment portfolio recommendation (e.g., 70% Tech, 30% Index).
3. A warning about market volatility.

STRATEGY:
"""

# Create the final prompt by injecting the distilled context
advice_prompt = PromptTemplate(
    input_variables=["distilled_context"],
    template=ADVICE_TEMPLATE
)

# Generate the final advice using the full, distilled context
final_advice_chain = advice_prompt | llm

print("\n" + "="*50)
print("--- 5.1: Generating Final Strategy using Distilled Context ---")
final_strategy = final_advice_chain.invoke({"distilled_context": distilled_context})
print(final_strategy)
print("="*50)
