
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

def exercise_1_memory(llm: ChatOpenAI):
    """
    Implements a persistent conversational interface using ConversationBufferMemory.
    """
    if not llm:
        print("LLM not initialized. Skipping Exercise 1.")
        return

    print("\n--- EXERCISE 1: Memory Abstraction ---")
    
    # 1. Memory Implementation: Stores history under the key 'chat_history'
    memory = ConversationBufferMemory(memory_key="chat_history")
    
    # 2. Chain Definition: Prompt includes the placeholder for history
    template = """You are a helpful customer service agent. 
    You must use the user's name and the context of their issue when responding.
    
    Chat History:
    {chat_history}
    
    New User Input: {input}
    
    Agent Response:"""
    
    prompt = PromptTemplate(input_variables=["chat_history", "input"], template=template)
    
    # We pass the memory object directly to the LLMChain
    conversation_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=False
    )
    
    # 3. Turn 1 (Setup)
    input_1 = "My name is Alex and I am having trouble logging into my account."
    print(f"User 1: {input_1}")
    response_1 = conversation_chain.invoke({"input": input_1})
    print(f"Agent Response 1: {response_1['text'].strip()}")
    
    # 4. Turn 2 (Context Retrieval)
    input_2 = "What steps should I take now?"
    print(f"\nUser 2: {input_2}")
    response_2 = conversation_chain.invoke({"input": input_2})
    print(f"Agent Response 2: {response_2['text'].strip()}")
    
    # 5. Output Validation
    print("\n--- Memory Validation (Full Buffer Contents) ---")
    print(memory.load_memory_variables({}))

# exercise_1_memory(llm)
