
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
import shutil
from typing import List, Dict, Any

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# --- Utility Functions (Copied from setup for context) ---

def create_sample_docs(corpus_name: str) -> List[Document]:
    """Creates a sample set of documents for indexing."""
    if corpus_name == "asyncio":
        texts = [
            "Asyncio is a library to write concurrent code using the async/await syntax. It is the foundation for multiple Python asynchronous frameworks.",
            "A Future represents an eventual result of an asynchronous operation. Awaitables are objects that can be awaited, including coroutines and Tasks.",
            "The event loop is the core of every asyncio application. It handles scheduling and execution of asynchronous tasks and callbacks.",
            "Standard threading requires OS-level context switching, which is inefficient compared to asyncio's single-thread cooperative multitasking model.",
            "While asyncio is great for I/O bound tasks, it offers no benefit for CPU-bound tasks, which should use multiprocessing instead."
        ]
        return [Document(page_content=t, metadata={"source": f"doc_{i}", "topic": "asyncio"}) for i, t in enumerate(texts)]
    
    # ... other corpus definitions omitted for brevity ...
    
    raise ValueError("Unknown corpus name")

def initialize_hf_embeddings(model_name: str) -> HuggingFaceEmbeddings:
    """Initializes a HuggingFace embedding model."""
    return HuggingFaceEmbeddings(model_name=model_name)

# --- Solution Implementation ---

def run_exercise_1_persistence_test(persist_dir: str):
    """
    Implements the persistence test for ChromaDB: indexing, saving, deleting, 
    reloading, and verifying data integrity.
    """
    # 1. Setup and Initial Indexing
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)
        
    documents = create_sample_docs("asyncio")
    embedding_model = initialize_hf_embeddings("all-MiniLM-L6-v2")
    
    print(f"--- Phase 1: Indexing and Initial Verification (Saving to {persist_dir}) ---")
    
    # Create and populate the persistent store
    vectorstore_1 = Chroma.from_documents(
        documents=documents, 
        embedding=embedding_model, 
        persist_directory=persist_dir
    )
    # CRITICAL STEP: Ensure data is written to disk
    vectorstore_1.persist() 
    
    query = "What is the main component that schedules tasks?"
    results_1 = vectorstore_1.similarity_search(query, k=1)
    
    # Verification (Phase 1)
    print(f"Result 1 (In-Memory): {results_1[0].page_content}")
    
    # 2. Persistence Test: Destroy references
    print("\nDestroying in-memory references...")
    del vectorstore_1
    del embedding_model
    
    # 3. Reload and Verification (Phase 2)
    print("\n--- Phase 2: Reloading from Disk and Verification ---")
    
    # Re-initialize the embedding model (needed for search function)
    reloaded_embedding_model = initialize_hf_embeddings("all-MiniLM-L6-v2")
    
    # Load the existing store from the persistence directory
    # Note: No documents passed here, it relies entirely on the persisted data
    vectorstore_2 = Chroma(
        persist_directory=persist_dir, 
        embedding_function=reloaded_embedding_model
    )
    
    # Run the same query
    results_2 = vectorstore_2.similarity_search(query, k=1)
    print(f"Result 2 (Reloaded): {results_2[0].page_content}")
    
    # 4. Metadata Check
    print(f"Metadata Check: {results_2[0].metadata}")

    if results_1[0].page_content == results_2[0].page_content:
         print("\nSUCCESS: Persistence and reload verified. The costly embedding step was skipped.")
    else:
         print("\nFAILURE: Reloaded content did not match original retrieval.")

# Execute the solution
# run_exercise_1_persistence_test("./chroma_data_ex1")
