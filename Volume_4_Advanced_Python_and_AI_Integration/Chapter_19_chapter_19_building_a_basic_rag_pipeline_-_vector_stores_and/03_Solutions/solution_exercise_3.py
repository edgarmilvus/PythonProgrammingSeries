
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

import os
import shutil
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List

# --- Utility Functions (Copied from setup for context) ---

def create_sample_docs(corpus_name: str) -> List[Document]:
    """Creates a sample set of documents, including intentional redundancy."""
    if corpus_name == "redundant":
        texts = [
            # Highly relevant, but redundant (A, C, E)
            "Section A: Introduction. The core principle of our system is security and resilience.", # Doc 0
            "Section B: Data Handling. All data must be encrypted at rest and in transit.",        # Doc 1 (Diverse)
            "Appendix 1: Security Overview. The core principle of our system is security and resilience. This is paramount.", # Doc 2 (Redundant to 0)
            "Section C: Performance Metrics. Latency targets must be met under 50ms.",             # Doc 3 (Diverse)
            "Appendix 2: Resilience Summary. We prioritize security and resilience above all else." # Doc 4 (Redundant to 0 and 2)
        ]
        return [Document(page_content=t, metadata={"source": f"doc_{i}", "category": "policy"}) for i, t in enumerate(texts)]
    
    # ... other corpus definitions omitted for brevity ...
    
    raise ValueError("Unknown corpus name")

def initialize_hf_embeddings(model_name: str) -> HuggingFaceEmbeddings:
    """Initializes a HuggingFace embedding model."""
    return HuggingFaceEmbeddings(model_name=model_name)

# --- Solution Implementation ---

def run_exercise_3_mmr_tuning(persist_dir: str):
    """
    Implements and compares standard similarity retrieval against MMR 
    with varying lambda_mult values.
    """
    
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    documents = create_sample_docs("redundant")
    embedding_model = initialize_hf_embeddings("all-MiniLM-L6-v2")
    
    # Create and populate the store
    vectorstore = Chroma.from_documents(
        documents=documents, 
        embedding=embedding_model, 
        persist_directory=persist_dir
    )
    
    query = "What is the most important guiding principle of the company?"
    k_val = 3 # Retrieve 3 documents

    print("\n--- Exercise 3: MMR Retrieval Comparison ---")
    
    # 1. Standard Similarity Baseline (Should return redundant documents based purely on score)
    retriever_sim = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k_val})
    results_sim = retriever_sim.invoke(query)
    print(f"\n[Baseline: Similarity Search (k={k_val})]")
    for i, doc in enumerate(results_sim):
        print(f"Doc {i+1}: {doc.page_content[:40]}... (Source: {doc.metadata['source']})")

    # 2. MMR - High Relevance (lambda_mult = 0.75) - Still favors similarity heavily
    retriever_mmr_high_rel = vectorstore.as_retriever(
        search_type="mmr", 
        search_kwargs={"k": k_val, "lambda_mult": 0.75}
    )
    results_mmr_high_rel = retriever_mmr_high_rel.invoke(query)
    print(f"\n[MMR: High Relevance (lambda_mult=0.75)]")
    for i, doc in enumerate(results_mmr_high_rel):
        print(f"Doc {i+1}: {doc.page_content[:40]}... (Source: {doc.metadata['source']})")

    # 3. MMR - High Diversity (lambda_mult = 0.25) - Prioritizes diversity strongly
    retriever_mmr_high_div = vectorstore.as_retriever(
        search_type="mmr", 
        search_kwargs={"k": k_val, "lambda_mult": 0.25}
    )
    results_mmr_high_div = retriever_mmr_high_div.invoke(query)
    print(f"\n[MMR: High Diversity (lambda_mult=0.25)]")
    for i, doc in enumerate(results_mmr_high_div):
        print(f"Doc {i+1}: {doc.page_content[:40]}... (Source: {doc.metadata['source']})")

    print("\n--- Analysis ---")
    print("Standard Similarity: Likely retrieves Docs 0, 2, and 4 (all highly relevant and redundant).")
    print("MMR (High Relevance): May slightly diversify, but often returns similar results to baseline.")
    print("MMR (High Diversity): Should retrieve the most relevant document (e.g., Doc 0), and then prioritize the next most diverse documents (e.g., Doc 1: Data Handling, or Doc 3: Performance Metrics), successfully excluding redundant security/resilience sections.")

# Execute the solution
# run_exercise_3_mmr_tuning("./chroma_data_ex3")
