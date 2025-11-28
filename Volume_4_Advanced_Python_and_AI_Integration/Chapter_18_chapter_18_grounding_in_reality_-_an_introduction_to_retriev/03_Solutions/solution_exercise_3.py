
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

# Source File: solution_exercise_3.py
# Description: Solution for Exercise 3
# ==========================================

print("--- Exercise 2: Vectorization and Semantic Search ---")

# 1. Define Knowledge Base
programming_chunks = [
    "Python's use of classes, inheritance, and polymorphism defines Object-Oriented Programming (OOP). These are core design principles for modularity.",
    "Functional Programming emphasizes pure functions, immutability, and avoiding shared state, leading to easily testable code.",
    "Procedural programming relies on sequences of steps, procedures, and routine calls, often using global state variables.",
    "The concept of dependency injection helps manage complex relationships between classes in large software architectures.",
    "A generator in Python is a function that returns an iterator, used for memory-efficient iteration over large datasets."
]

# 2. & 3. Indexing (Using Chroma in memory)
print("Indexing programming chunks...")
vectorstore = Chroma.from_texts(
    texts=programming_chunks,
    embedding=EMBEDDING_MODEL,
    collection_name="programming_concepts"
)
print("Indexing complete.")

# 4. Semantic Query
query_semantic = "What are the best practices for structuring large codebases?"
print(f"\nQuery: '{query_semantic}'")

# 5. Verification (Similarity Search)
retrieved_docs = vectorstore.similarity_search(query_semantic, k=3)

print("\nTop 3 Retrieved Documents (Semantic Search):")
for i, doc in enumerate(retrieved_docs):
    print(f"Result {i+1} (Score: {doc.metadata.get('score', 'N/A')}): {doc.page_content}")
    
# Analysis: The top results should relate to OOP and dependency injection, proving 
# semantic understanding of 'structuring large codebases' rather than just keyword matching.

print("-" * 60)
