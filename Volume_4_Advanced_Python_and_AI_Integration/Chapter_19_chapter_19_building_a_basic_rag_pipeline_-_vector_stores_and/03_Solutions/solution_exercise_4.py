
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

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import shutil
import os

# Define a technical document with nested structure and specific details
TECHNICAL_DOC = """
# Project Chronos: System Architecture V2.1

## 1. Introduction
This document outlines the architecture for Chronos, focusing on modularity and scalability. The core system runs on a microservice mesh.

## 2. Data Persistence Layer
All relational data is stored in PostgreSQL. Non-relational, high-volume telemetry data is handled by a dedicated time-series database.

### 2.1. Telemetry Data Handling
Telemetry ingestion uses a Kafka pipeline. Specifically, the buffer size for Kafka topic 'telemetry_stream' MUST NOT exceed 10 megabytes per partition to prevent back-pressure. This is a critical operational constraint.

## 3. Security Protocols
Authentication is managed via OAuth2 tokens. All internal service-to-service communication is secured using mutual TLS (mTLS).
"""

def create_single_doc() -> List[Document]:
    """Creates a single document for splitting."""
    return [Document(page_content=TECHNICAL_DOC, metadata={"source": "chronos_v2.1"})]

def index_and_query_recursive(
    chunk_size: int, 
    chunk_overlap: int, 
    persist_dir: str, 
    query: str
) -> List[Document]:
    """Indexes documents using RecursiveCharacterTextSplitter and performs a query."""
    
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    # 1. Refactor Splitter and Define Separators
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],  # Prioritize large breaks first
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    
    documents = create_single_doc()
    chunks = text_splitter.split_documents(documents)
    
    print(f"Indexing with size={chunk_size}, overlap={chunk_overlap}. Total chunks: {len(chunks)}")
    
    embedding_model = initialize_hf_embeddings("all-MiniLM-L6-v2")
    
    # Indexing
    vectorstore = Chroma.from_documents(chunks, embedding_model, persist_directory=persist_dir)
    vectorstore.persist()
    
    # Retrieval
    results = vectorstore.similarity_search(query, k=2)
    return results, len(chunks)

def run_exercise_4_chunking_optimization():
    """Runs the two chunking experiments and compares results."""
    
    long_tail_query = "What is the specific buffer limit for the telemetry stream?"

    # Experiment 1: Large Chunks / Minimal Overlap
    print("\n--- Experiment 1: Large Chunks (2000/50) ---")
    results_1, count_1 = index_and_query_recursive(
        chunk_size=2000, 
        chunk_overlap=50, 
        persist_dir="./chroma_data_ex4_exp1", 
        query=long_tail_query
    )
    print(f"Total Chunks Generated: {count_1}")
    print("Retrieval 1 (Large Chunk):")
    for i, doc in enumerate(results_1):
        print(f"  Doc {i+1}: Length {len(doc.page_content)}. Content starts: {doc.page_content[:100]}...")
        
    # Experiment 2: Small, Overlapping Chunks
    print("\n--- Experiment 2: Small Chunks (500/150) ---")
    results_2, count_2 = index_and_query_recursive(
        chunk_size=500, 
        chunk_overlap=150, 
        persist_dir="./chroma_data_ex4_exp2", 
        query=long_tail_query
    )
    print(f"Total Chunks Generated: {count_2}")
    print("Retrieval 2 (Small, Overlapping Chunk):")
    for i, doc in enumerate(results_2):
        print(f"  Doc {i+1}: Length {len(doc.page_content)}. Content starts: {doc.page_content[:100]}...")

    print("\n--- Comparative Analysis ---")
    print(f"Chunk Count Comparison: Exp 1 ({count_1}) vs. Exp 2 ({count_2})")
    print("Small chunks (Exp 2) generated more chunks, leading to a larger index, but potentially better retrieval granularity.")
    print("Retrieval Quality: The specific detail (buffer limit) is likely buried in a large chunk in Exp 1, diluting its semantic signal. In Exp 2, the small chunk size isolates the specific detail, and the high overlap (150) ensures the section heading ('Telemetry Data Handling') remains attached to the core detail, improving precision.")

# Execute the solution
# run_exercise_4_chunking_optimization()
