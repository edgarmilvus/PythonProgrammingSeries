
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

# Source File: solution_exercise_1.py
# Description: Solution for Exercise 1
# ==========================================

import os
from langchain_openai import OpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory
)
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables (assuming OPENAI_API_KEY is set)
load_dotenv()

# Initialize the LLM
try:
    # Using low temperature for predictable memory simulation
    llm = OpenAI(temperature=0.0)
except Exception as e:
    print(f"Error initializing LLM. Ensure OPENAI_API_KEY is set: {e}")
    llm = None
    print("Warning: LLM operations will be skipped due to initialization failure.")

# --- Utility Function for LLM Check ---
def check_llm_initialized():
    """Checks if the LLM object is ready for use."""
    if not llm:
        print("Skipping execution: LLM not initialized.")
        return False
    return True

# ====================================================================
## Exercise 1: Manual Context Injection and the DRY Principle
# ====================================================================

def execute_analysis_chain(chain, user_input, memory):
    """
    Executes a chain by manually retrieving history and injecting it
    into the input payload, then saving the new exchange.
    Adheres to DRY by centralizing memory management.
    """
    if not check_llm_initialized():
        return "LLM not initialized."

    # 1. Retrieve history
    history_dict = memory.load_memory_variables({})

    # 2. Prepare input dictionary using dict.update() (DRY principle)
    input_payload = {"input": user_input}
    # Merge history (e.g., {'history': '...'}) into the payload
    input_payload.update(history_dict)

    # 3. Execute the chain
    print(f"\n--- Running Chain with Context (History Length: {len(history_dict['history'].splitlines())} lines) ---")
    response = chain.invoke(input_payload)
    chain_output = response['text']

    # 4. Save the new exchange
    memory.save_context({"input": user_input}, {"output": chain_output})

    return chain_output

# 1. Initialize a ConversationBufferMemory object
memory_e1 = ConversationBufferMemory()

# 2. Simulate initial conversation (two turns)
memory_e1.save_context(
    {"input": "Hi, my name is Alex and I specialize in advanced robotics."},
    {"output": "Hello Alex. Robotics is fascinating."}
)
memory_e1.save_context(
    {"input": "I need help debugging a complex asynchronous task flow."},
    {"output": "I am ready to assist with your async debugging."}
)

# 3. Define a simple LLMChain (Chain A)
prompt_template_1 = PromptTemplate(
    input_variables=["history", "input"],
    template="""You are a detailed analyst. Use the following history to contextualize the request:
{history}
User Request: {input}
Detailed Analysis:"""
)
chain_a = LLMChain(llm=llm, prompt=prompt_template_1, verbose=False) if llm else None

if check_llm_initialized():
    print("--- Exercise 1: Manual Context Injection ---")

    # Execute analysis chain (Turn 3)
    output_1 = execute_analysis_chain(
        chain_a,
        "Based on my specialty, what is the most challenging aspect of async programming?",
        memory_e1
    )
    print(f"Chain Output 1: {output_1.strip()}")

    # Execute analysis chain (Turn 4)
    output_2 = execute_analysis_chain(
        chain_a,
        "Considering the previous analysis, how does the GIL affect my async flow?",
        memory_e1
    )
    print(f"Chain Output 2: {output_2.strip()}")

    # 5. Verify final memory state
    print("\n--- Final Memory State (E1 Verification) ---")
    final_history = memory_e1.load_memory_variables({})['history']
    print(final_history)
    print(f"\nTotal exchanges saved: {len(final_history.splitlines()) // 2}")


# ====================================================================
## Exercise 2: Context Compression using Summary Memory
# ====================================================================

if check_llm_initialized():
    print("\n\n--- Exercise 2: Context Compression using Summary Memory ---")

    # 1. Initialize Summary Memory
    memory_e2 = ConversationSummaryMemory(llm=llm)
    chain_e2 = ConversationChain(llm=llm, memory=memory_e2, verbose=False)

    # 2. Simulate long conversation (5 verbose exchanges)
    print("Running Long Conversation Simulation...")

    # Turn 1 & 2 (Flask Blueprint issue)
    chain_e2.invoke("I am having trouble with my Flask server blueprint setup. I organized my routes into 'auth' and 'data' blueprints, but they seem to be conflicting due to duplicate endpoint names.")
    chain_e2.invoke("The conflict happens because I used the same endpoint name, 'status', in both blueprints. How do I resolve this without renaming the files?")

    # Turn 3 & 4 (Async file uploads)
    chain_e2.invoke("Thank you. I also need to know the best way to handle large file uploads asynchronously in Python, perhaps using a dedicated queue.")
    chain_e2.invoke("I am considering using Celery for background tasks. Is that overkill for simple file uploads, or is it necessary for robustness?")

    # Turn 5 (Project structure)
    chain_e2.invoke("Finally, I need a summary of the best practices for structuring a large Python project using the 'src' layout, including configuration management.")

    # 4. Retrieve and print summary
    summary_dict = memory_e2.load_memory_variables({})
    summary = summary_dict['history']
    print("\n--- Summary Memory Output (E2 Verification) ---")
    print(summary)

    # 5. Token/Word Count Estimation (Approximation)
    summary_word_count = len(summary.split())

    # Estimate Raw History: Assuming 5 verbose inputs (avg 25 words) and 5 verbose outputs (avg 75 words)
    # Total estimated raw words = (5 * 25) + (5 * 75) = 125 + 375 = 500 words
    estimated_raw_word_count = 500

    print(f"\nEstimated Raw History Words (if Buffer Memory): {estimated_raw_word_count}")
    print(f"Actual Summary Words: {summary_word_count}")

    if estimated_raw_word_count > summary_word_count:
        compression = ((estimated_raw_word_count - summary_word_count) / estimated_raw_word_count) * 100
        print(f"Compression achieved: {compression:.2f}% reduction.")
    else:
        print("Summary is unexpectedly longer than the estimated raw history.")


# ====================================================================
## Exercise 3: Focused Interaction with Windowed Memory
# ====================================================================

if check_llm_initialized():
    print("\n\n--- Exercise 3: Focused Interaction with Windowed Memory ---")

    # 1. Initialize Window Memory (k=3)
    # k=3 means it stores the last 3 user/AI exchanges (6 messages total).
    memory_e3 = ConversationBufferWindowMemory(k=3)
    chain_e3 = ConversationChain(llm=llm, memory=memory_e3, verbose=False)

    print("Running Windowed Conversation (k=3)...")

    # Turn 1: Topic A introduced (k=1)
    chain_e3.invoke("Turn 1: My favorite color is blue, and I am a software engineer.")
    # Turn 2: Topic A refined (k=2)
    chain_e3.invoke("Turn 2: I primarily work with Python and specifically enjoy the asyncio library.")
    # Turn 3: Topic A concluded (k=3)
    chain_e3.invoke("Turn 3: I use the term 'Coroutine' frequently in my work.")

    # Turn 4: Topic B introduced (k=3, Turn 1 is dropped from window)
    chain_e3.invoke("Turn 4: What is the capital of France?")

    # Turn 5: Topic B discussed (k=3, Turn 2 is dropped from window)
    chain_e3.invoke("Turn 5: Now, tell me about the architecture of the Eiffel Tower.")

    # 4. Verify memory state (Should only contain Turns 3, 4, 5)
    print("\n--- Window Memory State (E3 Verification) ---")
    final_history_e3 = memory_e3.load_memory_variables({})['history']
    print(final_history_e3)
    print(f"\nTotal exchanges visible: {len(final_history_e3.splitlines()) // 2}")
    # Verification: Turn 1 and Turn 2 context should be gone.

    # 5. Bonus: Query relying on forgotten context (Turn 1)
    print("\n--- Bonus Query (Testing Forgotten Context) ---")
    response_forgotten = chain_e3.invoke("What is my favorite color?")
    print(f"Model Response: {response_forgotten['response'].strip()}")
    # The model should state it doesn't recall, or guess incorrectly, 
    # proving the initial context (blue) was pruned.


# ====================================================================
## Exercise 4: Interactive Challenge - Dynamic Memory Switching
# ====================================================================

def initialize_chain(llm, memory_type: str, window_k: int = 5) -> ConversationChain:
    """
    Factory function to dynamically initialize a ConversationChain
    with the specified memory type.
    """
    if memory_type == 'buffer':
        memory = ConversationBufferMemory()
    elif memory_type == 'summary':
        if not llm:
            raise RuntimeError("LLM required for ConversationSummaryMemory.")
        memory = ConversationSummaryMemory(llm=llm)
    elif memory_type == 'window':
        if window_k < 1:
            raise ValueError("Window size 'k' must be at least 1.")
        memory = ConversationBufferWindowMemory(k=window_k)
    else:
        raise ValueError(f"Invalid memory type specified: {memory_type}. Must be 'buffer', 'summary', or 'window'.")

    # Initialize the chain with the dynamically created memory object
    return ConversationChain(llm=llm, memory=memory, verbose=False)

if check_llm_initialized():
    print("\n\n--- Exercise 4: Dynamic Memory Initialization ---")

    # 1. Initialize Chain Summary
    try:
        chain_summary = initialize_chain(llm, 'summary')
        print("Initialized chain_summary successfully.")
    except Exception as e:
        print(f"Error initializing summary chain: {e}")
        chain_summary = None

    # 2. Initialize Chain Window (k=2)
    try:
        chain_window = initialize_chain(llm, 'window', window_k=2)
        print("Initialized chain_window successfully.")
    except Exception as e:
        print(f"Error initializing window chain: {e}")
        chain_window = None

    # 3. Run brief conversation on both
    if chain_summary and chain_window:
        conversation_turns = [
            "Turn 1: My project name is 'Project Chimera'.",
            "Turn 2: I need to refactor the database layer.",
            "Turn 3: What was the name of my project?" # Query relies on Turn 1
        ]

        print("\n--- Testing Summary Chain (3 turns) ---")
        for turn in conversation_turns:
            chain_summary.invoke(turn)

        # Summary should contain a concise summary of all three turns
        summary_memory_output = chain_summary.memory.load_memory_variables({})
        print("Summary Chain Memory (History contains summary):", summary_memory_output)

        print("\n--- Testing Window Chain (k=2, 3 turns) ---")
        for turn in conversation_turns:
            chain_window.invoke(turn)

        # Window (k=2) should only contain the last two exchanges (Turns 2 and 3)
        window_memory_output = chain_window.memory.load_memory_variables({})
        print("Window Chain Memory (History contains last 2 exchanges):", window_memory_output)

        # Verification: The window memory should show context only from Turn 2 onwards.
