
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

print("--- Exercise 1: Chunking Mastery ---")

source_text = """
Section 1: The RAG Architecture Overview.
Retrieval-Augmented Generation (RAG) is a powerful paradigm designed to ground Large Language Models (LLMs)
in external, verifiable knowledge. This overcomes the LLM's inherent limitations, such as knowledge cutoff and
the tendency to hallucinate. The process involves three main stages: Indexing, Retrieval, and Generation.

Section 2: The Role of Vector Stores.
Vector databases, such as Chroma or Pinecone, are specialized stores optimized for high-dimensional data.
They are essential for RAG because they allow for rapid semantic search. Instead of searching for keywords,
we search for the meaning represented by the vector embeddings. This allows for flexible and context-aware retrieval.

Section 3: Advanced Splitters.
While simple splitters exist, the RecursiveCharacterTextSplitter is generally preferred for technical documents.
It attempts to preserve structural integrity by splitting first on large separators (like double newlines),
then smaller ones (single newlines), and finally characters. This hierarchical approach minimizes the chance
of breaking up semantically related sentences.
"""

# 1. Initial Split (Small Chunks: 150 size, 20 overlap)
splitter_small = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=20,
    separators=["\n\n", "\n", " ", ""]
)
docs_small = splitter_small.create_documents([source_text])
print(f"Total small chunks generated: {len(docs_small)}")

# 2. Coherence Analysis
print("\nFirst three small chunks (Potential for broken context):")
for i, doc in enumerate(docs_small[:3]):
    print(f"Chunk {i+1}: {doc.page_content}")

# Analysis: Chunk 2 clearly breaks a sentence: "The process involves three main stages: Indexing, Retrieval, and Generation."
# This shows that small chunks can lead to loss of immediate context.

# 3. Optimized Split (Large Chunks: 800 size, 100 overlap)
splitter_large = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
)
docs_large = splitter_large.create_documents([source_text])
print(f"\nTotal large chunks generated: {len(docs_large)}")

# 4. Overlap Verification
if len(docs_large) >= 2:
    chunk_a = docs_large[0].page_content
    chunk_b = docs_large[1].page_content
    
    # Calculate overlap
    overlap_size = 100
    overlap_a = chunk_a[-overlap_size:]
    overlap_b = chunk_b[:overlap_size]
    
    print("\nOverlap Verification:")
    print(f"End of Chunk A (Last {overlap_size} chars): '{overlap_a.strip()[:30]}...'")
    print(f"Start of Chunk B (First {overlap_size} chars): '{overlap_b.strip()[:30]}...'")
    
    # Simple check for content similarity in the overlap region
    match = overlap_a.strip() == overlap_b.strip()
    print(f"Overlap Match Status: {match}")
    print("The overlap ensures that if a critical sentence spans the boundary, both chunks contain enough context for the retriever.")

print("-" * 60)
