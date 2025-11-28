
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
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# --- 0. Environment Setup and LLM Initialization ---
# Assuming the necessary API key is set in the environment.
# We use a low temperature (0.0) to ensure predictable recall behavior.
llm = ChatOpenAI(temperature=0.0, model="gpt-3.5-turbo")

# --- 1. The Problem: Stateless Interaction (Demonstrates Failure) ---
print("--- SCENARIO 1: STATSLESS INTERACTION (No Memory) ---")

# Define a simple template without a history variable
stateless_template = """
You are a helpful, but forgetful, assistant.
Human: {input}
AI:"""

stateless_prompt = PromptTemplate(
    input_variables=["input"],
    template=stateless_template,
)

# Create a basic chain without specifying a memory object
stateless_chain = LLMChain(llm=llm, prompt=stateless_prompt)

# Interaction 1: Setting the context
user_input_1 = "My dog's name is Archimedes."
response1 = stateless_chain.invoke({"input": user_input_1})
print(f"User 1: {user_input_1}")
print(f"AI 1: {response1['text'].strip()}")

# Interaction 2: Asking a follow-up question that requires context
user_input_2 = "What is my dog's name?"
response2 = stateless_chain.invoke({"input": user_input_2})
print(f"\nUser 2: {user_input_2}")
print(f"AI 2 (Stateless Failure): {response2['text'].strip()}")
print("Expected Failure: The AI cannot recall the name 'Archimedes'.")

# --- 2. The Solution: Stateful Interaction using ConversationBufferMemory ---
print("\n" + "="*70)
print("--- SCENARIO 2: STATEFUL INTERACTION (With ConversationBufferMemory) ---")

# Initialize the memory object. 
# CRITICAL: Define the memory_key. This key dictates the variable name 
# that MUST be used in the prompt template to inject the history.
memory = ConversationBufferMemory(memory_key="chat_history")

# Define the template that explicitly includes the history variable
stateful_template = """
You are a helpful and conversational assistant.
The following is a conversation history between you and a Human:
{chat_history}
Human: {input}
AI:"""

# Note the input variables now include both 'chat_history' and 'input'
stateful_prompt = PromptTemplate(
    input_variables=["chat_history", "input"],
    template=stateful_template,
)

# Create the chain, injecting the memory object
stateful_chain = LLMChain(
    llm=llm, 
    prompt=stateful_prompt, 
    memory=memory,
    verbose=False
)

# Interaction 1: Setting the context (Memory is automatically updated)
user_input_3 = "I work as a quantum cryptography expert."
response3 = stateful_chain.invoke({"input": user_input_3})
print(f"User 1: {user_input_3}")
print(f"AI 1: {response3['text'].strip()}")

# Interaction 2: Asking a follow-up question that requires context
# The chain automatically fetches the history, inserts it into the prompt, 
# sends the combined text to the LLM, and then saves the new turn.
user_input_4 = "What is my profession?"
response4 = stateful_chain.invoke({"input": user_input_4})
print(f"\nUser 2: {user_input_4}")
print(f"AI 2 (Stateful Success): {response4['text'].strip()}")
print("Expected Success: The AI successfully recalls the profession.")


# --- 3. Inspecting and Managing the Memory State ---
print("\n" + "-"*70)
print("--- INSPECTING THE RAW MEMORY BUFFER ---")

# The load_memory_variables method returns the current state of the memory.
raw_memory = memory.load_memory_variables({})
print(f"Memory Key Used: {list(raw_memory.keys())[0]}")
print("--- Full Conversation History Stored (Formatted as a single string) ---")
print(raw_memory["chat_history"])

# Resetting the memory state
memory.clear()
print("\nMemory Cleared. New state:")
print(memory.load_memory_variables({}))
