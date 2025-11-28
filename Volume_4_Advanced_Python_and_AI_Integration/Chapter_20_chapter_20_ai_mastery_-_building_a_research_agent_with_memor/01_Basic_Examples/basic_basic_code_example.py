
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
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# --- 1. Setup and Configuration ---
# Ensure your OpenAI API key is available in your environment variables.
if 'OPENAI_API_KEY' not in os.environ:
    # In a real deployment, this check would raise an error. 
    # For this educational example, we provide a warning.
    print("WARNING: OPENAI_API_KEY environment variable not set.")


# --- 2. Define the Conversational Components ---

# The template must explicitly include the {history} variable. 
# This variable acts as the placeholder where the ConversationChain will inject 
# the accumulated chat log retrieved from the memory object.
template = """You are a sophisticated, friendly assistant named 'Aura'. 
You maintain context throughout the conversation.
Current Conversation:
{history}
Human: {input}
Aura:"""

# Initialize the Prompt Template
PROMPT = PromptTemplate(
    input_variables=["history", "input"], 
    template=template
)

# Initialize the LLM
# We use a fast model (gpt-3.5-turbo) suitable for high-volume conversational tasks.
llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")

# --- 3. Implement Memory ---

# ConversationBufferMemory is the simplest form; it stores all previous 
# messages (Human and AI) as a raw text string.
memory = ConversationBufferMemory()

# --- 4. Create the Stateful Chain ---

# The ConversationChain orchestrates the flow: input -> memory retrieval -> prompt assembly -> LLM call -> memory storage.
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=PROMPT,
    verbose=True # Setting verbose=True allows us to inspect the full prompt sent to the LLM.
)

print("--- Starting Conversation (Stateful) ---")

# --- 5. Sequential Interactions Demonstrating Memory ---

# Interaction 1: Introduction of a specific, complex technical topic (EAFP/LBYL)
query_1 = "I am learning Python. What is the fundamental difference between EAFP and LBYL coding styles?"
response_1 = conversation.invoke({"input": query_1})
print(f"\n[Human]: {query_1}")
print(f"[Aura]: {response_1['response']}")

# Interaction 2: Follow-up question relying entirely on the context established in Interaction 1.
# The agent must remember the context (EAFP/LBYL) to answer correctly.
query_2 = "Which of those styles is generally preferred in the Python community, and why?"
response_2 = conversation.invoke({"input": query_2})
print(f"\n[Human]: {query_2}")
print(f"[Aura]: {response_2['response']}")

# Interaction 3: Checking the stored history manually
print("\n--- Current Memory State (Raw History) ---")
# load_memory_variables returns a dictionary containing the memory content, 
# keyed by the variable name used in the prompt (default is 'history').
history_data = memory.load_memory_variables({})
print(history_data)

# Interaction 4: A new, unrelated question to demonstrate general conversational ability
query_3 = "Separately, how many integers are there between 10 and 20, inclusive?"
response_3 = conversation.invoke({"input": query_3})
print(f"\n[Human]: {query_3}")
print(f"[Aura]: {response_3['response']}")
