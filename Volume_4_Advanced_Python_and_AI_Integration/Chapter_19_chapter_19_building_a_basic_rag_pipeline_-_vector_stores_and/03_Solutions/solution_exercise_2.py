
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

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List

def initialize_hf_embeddings(model_name: str) -> HuggingFaceEmbeddings:
    """Initializes a HuggingFace embedding model."""
    return HuggingFaceEmbeddings(model_name=model_name)

def run_exercise_2_model_comparison():
    """
    Compares retrieval results and scores between two different embedding models.
    """
    # 1. Corpus Definition (Asyncio corpus from Exercise 1)
    documents = create_sample_docs("asyncio")
    
    # Query: Targeted at non-blocking I/O, expecting doc 3 (event loop) or doc 4 (threading comparison)
    query = "What is the non-blocking I/O paradigm in Python?"

    # 2. Model Selection
    # Model A: Smaller, faster
    model_A_name = "all-MiniLM-L6-v2"
    # Model B: Larger, potentially richer semantic space
    model_B_name = "all-mpnet-base-v2"

    emb_A = initialize_hf_embeddings(model_A_name)
    emb_B = initialize_hf_embeddings(model_B_name)
    
    # 3. Dual Indexing (Using in-memory stores for simplicity)
    vectorstore_A = Chroma.from_documents(documents=documents, embedding=emb_A)
    vectorstore_B = Chroma.from_documents(documents=documents, embedding=emb_B)

    # 4 & 5. Query Execution and Comparative Retrieval (k=3)
    k_val = 3
    
    print(f"--- Retrieval Results for Query: '{query}' ---")
    
    # Store A Retrieval
    results_A = vectorstore_A.similarity_search_with_score(query, k=k_val)
    print(f"\n[Model A: {model_A_name}]")
    for doc, score in results_A:
        # Note: Chroma returns L2 distance, where lower score means higher similarity
        print(f"  Score: {score:.4f} | Content: {doc.page_content[:60]}...")

    # Store B Retrieval
    results_B = vectorstore_B.similarity_search_with_score(query, k=k_val)
    print(f"\n[Model B: {model_B_name}]")
    for doc, score in results_B:
        print(f"  Score: {score:.4f} | Content: {doc.page_content[:60]}...")

    # 6. Analysis (Based on typical model performance)
    print("\n--- Comparative Analysis ---")
    print("Model A (MiniLM) is generally trained for speed and basic similarity.")
    print("Model B (MPNet) is larger, often capturing subtle semantic relationships better.")
    print("Observation: Differences in scores and ranking demonstrate how each model interprets 'non-blocking I/O'.")
    print("The document about 'CPU-bound tasks' (tangentially related) might rank differently because one model might strongly associate 'I/O bound' with the query, while the other focuses more on the 'asynchronous' nature.")

# Execute the solution
# run_exercise_2_model_comparison()
