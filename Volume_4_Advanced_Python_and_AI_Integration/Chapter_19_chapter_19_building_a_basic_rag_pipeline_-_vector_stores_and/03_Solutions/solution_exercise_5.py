
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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

import os
import shutil
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List

# --- Utility Functions (Copied from setup for context) ---
def create_sample_docs(corpus_name: str) -> List[Document]:
    # ... (definition of documents omitted for brevity) ...
    if corpus_name == "asyncio":
        texts = [
            "Asyncio is a library to write concurrent code using the async/await syntax. It is the foundation for multiple Python asynchronous frameworks.",
            "A Future represents an eventual result of an asynchronous operation. Awaitables are objects that can be awaited, including coroutines and Tasks.",
            "The event loop is the core of every asyncio application. It handles scheduling and execution of asynchronous tasks and callbacks.",
            "Standard threading requires OS-level context switching, which is inefficient compared to asyncio's single-thread cooperative multitasking model.",
            "While asyncio is great for I/O bound tasks, it offers no benefit for CPU-bound tasks, which should use multiprocessing instead."
        ]
        return [Document(page_content=t, metadata={"source": f"doc_{i}", "topic": "asyncio"}) for i, t in enumerate(texts)]
    raise ValueError("Unknown corpus name")

def initialize_hf_embeddings(model_name: str) -> HuggingFaceEmbeddings:
    """Initializes a HuggingFace embedding model."""
    return HuggingFaceEmbeddings(model_name=model_name)

# --- Solution Implementation ---

def run_exercise_5_faiss_persistence(faiss_path: str):
    """
    Implements FAISS indexing, manual serialization (save_local), 
    and deserialization (load_local).
    """
    
    # Increase volume for a more realistic FAISS use case (50 chunks)
    documents = create_sample_docs("asyncio") * 10 
    embedding_model = initialize_hf_embeddings("all-MiniLM-L6-v2")
    
    if os.path.exists(faiss_path):
        shutil.rmtree(faiss_path)
    
    print("\n--- Phase 1: FAISS In-Memory Indexing and Saving ---")
    
    # 1. FAISS Indexing (In-memory)
    faiss_index_1 = FAISS.from_documents(documents, embedding_model)
    query = "What is the event loop?"
    
    # In-Memory Retrieval verification
    results_1 = faiss_index_1.similarity_search(query, k=1)
    print(f"Result 1 (In-Memory): {results_1[0].page_content[:50]}...")
    
    # 2. Manual Persistence (Serialization)
    faiss_index_1.save_local(faiss_path, index_name="asyncio_index")
    print(f"FAISS index saved to {faiss_path}")
    
    # 3. Destroy references
    del faiss_index_1
    del embedding_model

    # 4. Manual Reload (Deserialization)
    print("\n--- Phase 2: Reloading FAISS Index ---")
    reloaded_embedding_model = initialize_hf_embeddings("all-MiniLM-L6-v2")
    
    # Note: FAISS requires the embedding function used for indexing to be passed during load
    faiss_index_2 = FAISS.load_local(
        faiss_path, 
        reloaded_embedding_model, 
        index_name="asyncio_index"
    )
    
    # 5. Verification
    results_2 = faiss_index_2.similarity_search(query, k=1)
    print(f"Result 2 (Reloaded): {results_2[0].page_content[:50]}...")

    if results_1[0].page_content == results_2[0].page_content:
         print("\nSUCCESS: FAISS manual serialization/deserialization verified.")
    else:
         print("\nFAILURE: Reloaded content did not match original retrieval.")
    
    # Cleanup
    if os.path.exists(faiss_path):
        shutil.rmtree(faiss_path)

    print("\n--- Discussion: FAISS vs. ChromaDB ---")
    print("FAISS Advantage: Extremely fast vector search due to optimized C++ backend, ideal for high-volume, performance-critical retrieval (e.g., massive datasets or real-time systems).")
    print("FAISS Disadvantage: Lacks automatic persistence; requires manual serialization (`save_local`) and deserialization (`load_local`). The embedding function must be explicitly provided during reload.")
    print("ChromaDB Advantage: Offers integrated persistence (automatic saving/loading) and a simpler setup, making it ideal for development and smaller, local RAG systems.")

# Execute the solution
# run_exercise_5_faiss_persistence("./faiss_index_ex5")
