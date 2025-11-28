
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

print("--- Exercise 3: Minimal RAG Chain (RetrievalQA) ---")

# 1. Retriever Setup (Using the vectorstore from Exercise 2)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 2. & 3. Chain Construction
# Note: We use the default prompt which encourages grounding, but Test 2 confirms 
# the LLM's adherence to context.
qa_chain = RetrievalQA.from_chain_type(
    llm=LLM,
    chain_type="stuff",
    retriever=retriever
)

# 4. Test 1 (Grounded Query)
query_grounded = "What are the key characteristics of Functional Programming?"
print(f"\nTest 1 - Grounded Query: {query_grounded}")
# Note: The output structure of invoke() depends on the chain type, but RetrievalQA often returns a dict.
response_grounded = qa_chain.invoke({"query": query_grounded})
print(f"Answer: {response_grounded['result']}")

# 5. Test 2 (Ungrounded Query)
# We expect the LLM to state it cannot answer based on the provided context.
query_ungrounded = "What is the history of the Eiffel Tower?"
print(f"\nTest 2 - Ungrounded Query: {query_ungrounded}")
response_ungrounded = qa_chain.invoke({"query": query_ungrounded})
print(f"Answer: {response_ungrounded['result']}")

print("-" * 60)
