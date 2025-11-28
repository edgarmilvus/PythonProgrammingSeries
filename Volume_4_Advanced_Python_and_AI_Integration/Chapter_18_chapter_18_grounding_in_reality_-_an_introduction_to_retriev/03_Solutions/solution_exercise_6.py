
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

# Source File: solution_exercise_6.py
# Description: Solution for Exercise 6
# ==========================================

print("--- Exercise 5: Optimizing Retrieval Strategy with MMR ---")

# 1. Knowledge Base Refinement (Redundancy Test)
redundant_chunks = [
    # Highly similar chunks (Type 1: Decorators)
    "A class decorator in Python modifies a class definition, often used for adding methods or properties.",
    "Function decorators use the @syntax to wrap a function, executing code before and after the function runs.",
    "A decorator factory is a function that returns a decorator, allowing the decorator to accept arguments.",
    # Dissimilar chunks (Type 2: Asyncio/Generators)
    "Asyncio event loops manage concurrent tasks, scheduling coroutines to run efficiently.",
    "The 'await' keyword pauses execution of an async function until the awaited task is complete.",
    "Generators and iterators are fundamental to Python's memory management for large data streams."
]

# 2. Indexing
mmr_vectorstore = Chroma.from_texts(
    texts=redundant_chunks,
    embedding=EMBEDDING_MODEL,
    collection_name="mmr_test_concepts"
)

query_mmr = "Explain the different ways to modify functions using special Python syntax."

# 3. Similarity Retrieval (k=3)
# This will likely retrieve the three decorator chunks, but the ranking might favor
# two extremely similar decorator chunks, potentially missing one of the distinct types.
similarity_retriever = mmr_vectorstore.as_retriever(search_kwargs={'k': 3, 'search_type': 'similarity'})
sim_docs = similarity_retriever.invoke(query_mmr)

print("\n--- Similarity Search Results (Likely Redundant, focusing purely on relevance) ---")
for i, doc in enumerate(sim_docs):
    print(f"Doc {i+1}: {doc.page_content[:60]}...")

# 4. MMR Retrieval (k=3, fetch_k=10)
# MMR fetches 10 documents initially, then selects the best 3 based on relevance AND diversity.
mmr_retriever = mmr_vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={'k': 3, 'fetch_k': 10} # k=final result count, fetch_k=pool size
)
mmr_docs = mmr_retriever.invoke(query_mmr)

print("\n--- MMR Search Results (Balanced Diversity: Ensures all 3 decorator types are represented) ---")
for i, doc in enumerate(mmr_docs):
    print(f"Doc {i+1}: {doc.page_content[:60]}...")

# 5. Comparative Analysis
print("\nAnalysis:")
print("Standard Similarity: Ranks documents purely by relevance score. If two decorator chunks are extremely similar, they might both be selected, leading to redundant context.")
print("MMR: Selects the most relevant document first, then selects subsequent documents that are relevant but maximally dissimilar to those already selected. This ensures a broader, more diverse context set (e.g., guaranteeing all three distinct decorator types are retrieved).")

print("-" * 60)
