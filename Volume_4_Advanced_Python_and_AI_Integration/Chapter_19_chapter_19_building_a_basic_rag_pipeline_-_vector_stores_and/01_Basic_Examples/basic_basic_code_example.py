
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

# Source File: basic_basic_code_example.py
# Description: Basic Code Example
# ==========================================

import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from typing import List

# --- Configuration Constants ---
# Using a widely available and small embedding model
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2" 
K_RETRIEVAL = 2 # Number of documents to retrieve

# 1. Define the Source Data Corpus
# In a real application, this would be loaded from PDFs, databases, or large files.
raw_documents: List[str] = [
    "The Python programming language was created by Guido van Rossum and first released in 1991.",
    "FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering of dense vectors.",
    "Retrieval-Augmented Generation (RAG) enhances LLMs by grounding their answers in external data.",
    "Vector stores map text chunks to their numerical vector representations (embeddings)."
]

# 2. Prepare Documents for LangChain
# LangChain components typically operate on the Document object structure.
# We map the raw strings into Document objects.
def create_langchain_documents(texts: List[str]) -> List[Document]:
    """Converts a list of strings into LangChain Document objects."""
    # We assign a simple metadata key for identification, simulating a source path
    documents = [
        Document(
            page_content=text, 
            metadata={"source": f"doc_id_{i+1}"}
        ) 
        for i, text in enumerate(texts)
    ]
    return documents

documents = create_langchain_documents(raw_documents)
print(f"Prepared {len(documents)} LangChain documents for indexing.")

# 3. Initialize the Embedding Model
# This component is responsible for generating the dense vectors (embeddings).
# It must be the same model used for both indexing and querying.
try:
    embeddings_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    print(f"Successfully loaded embedding model: {EMBEDDING_MODEL_NAME}")
except Exception as e:
    # Handle potential issues if the model cannot be downloaded (e.g., network issues)
    print(f"Error loading HuggingFace model: {e}")
    # Exit or use a fallback mechanism here in a real scenario
    exit()

# 4. Build the FAISS Vector Store Index (The Indexing Phase)
# FAISS.from_documents performs two key tasks:
# a) Uses the embeddings_model to calculate the vector for every document.
# b) Stores these vectors in an optimized, searchable index structure in memory.
print("\n--- Starting Index Generation (Embedding and Storing) ---")
vector_store = FAISS.from_documents(
    documents=documents,
    embedding=embeddings_model
)
print("FAISS index built successfully in memory.")

# 5. Configure and Instantiate the Retriever
# The retriever is the operational interface to the vector store.
# It defines *how* the search should be executed.
retriever = vector_store.as_retriever(
    search_type="similarity", # Standard search based on vector distance
    search_kwargs={"k": K_RETRIEVAL} # Retrieve the top K most similar results
)

# 6. Perform a Retrieval Query (The Runtime Phase)
query = "Tell me about the creator of Python and what RAG aims to achieve."
print(f"\n--- Performing Retrieval Query: '{query}' ---")

# The 'invoke' method executes the retrieval logic:
# 1. Embeds the query using the same model.
# 2. Searches the FAISS index for the nearest vectors.
# 3. Returns the corresponding Document objects.
retrieved_docs = retriever.invoke(query)

# 7. Display Results
print(f"\nSuccessfully retrieved {len(retrieved_docs)} context documents.")
print("--- Retrieved Context Documents ---")
for i, doc in enumerate(retrieved_docs):
    # Displaying the content and the simulated source metadata
    print(f"Document {i+1} (Source: {doc.metadata.get('source', 'N/A')}):")
    print(f"Content Snippet: {doc.page_content[:80]}...")
    print("-" * 20)

# Example of a less relevant query (to show similarity search effectiveness)
less_relevant_query = "What is the purpose of the FAISS library?"
print(f"\n--- Performing Less Relevant Query: '{less_relevant_query}' ---")
less_relevant_docs = retriever.invoke(less_relevant_query)

print(f"Document 1 Content: {less_relevant_docs[0].page_content[:80]}...")
