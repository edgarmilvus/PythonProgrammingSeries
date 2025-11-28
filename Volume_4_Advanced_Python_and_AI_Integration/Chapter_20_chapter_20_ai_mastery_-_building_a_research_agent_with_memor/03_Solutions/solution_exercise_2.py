
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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

# 1. Memory Initialization
llm_for_summary = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# Set a small token limit (e.g., 100) to force summarization quickly
MAX_TOKENS = 100 
memory = ConversationSummaryBufferMemory(
    llm=llm_for_summary,
    max_token_limit=MAX_TOKENS,
    return_messages=True # Required for easy inspection
)

# 2. Chain Construction
conversation = ConversationChain(
    llm=llm_for_summary,
    memory=memory,
    verbose=False
)

# 3. Simulated Conversation (Long turns)
print("--- Starting Conversation (Turns 1 & 2 will trigger summarization) ---")

# Turn 1 (Long, descriptive turn)
response1 = conversation.invoke({
    "input": "The theoretical framework of quantum entanglement involves non-local correlations and the collapse of the wave function upon measurement. This concept fundamentally challenges classical physics' notion of locality and realism, suggesting a deeper, interconnected reality."
})
print(f"Turn 1 Response: {response1['response'][:50]}...")

# Turn 2 (Longer, ensuring token limit is breached)
response2 = conversation.invoke({
    "input": "That's fascinating. Specifically, the Bell inequalities test whether local hidden variable theories can explain entanglement. Experimental violations of these inequalities strongly support quantum mechanics."
})
print(f"Turn 2 Response: {response2['response'][:50]}...")

# Turn 3 (Short follow-up)
response3 = conversation.invoke({
    "input": "So, what are the practical applications of violating Bell's theorem?"
})
print(f"Turn 3 Response: {response3['response'][:50]}...")

# 4. Verification
print("\n--- Memory Inspection after Summarization Trigger ---")

# The memory buffer should now contain a summary message followed by recent turns.
if memory.buffer and hasattr(memory.buffer[0], 'type') and memory.buffer[0].type == 'system':
    summary_message = memory.buffer[0].content
    print(f"Total messages currently in buffer: {len(memory.buffer)}")
    print(f"Summary Message Content (First 150 chars): {summary_message[:150]}...")
else:
     print("Summarization did not appear to trigger as expected or memory structure is different.")

# Turn 5: Ask a question requiring recall
response5 = conversation.invoke({
    "input": "Based on our initial discussion, what was the main challenge to classical physics?"
})
print("\n--- Turn 5 (Recalling Summarized Context) ---")
print(f"Agent Response: {response5['response']}")
