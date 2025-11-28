
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

# Source File: project_advanced_application_script.py
# Description: Advanced Application Script
# ==========================================

import os
import shutil
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from typing import List

# 1. Configuration and Setup (Mock Data)
# NOTE: Ensure OPENAI_API_KEY is set in your environment variables.

# Simulated internal documentation text (acting as the raw knowledge base)
POLICY_TEXT = """
Section 1: Data Governance Policy. All PII must be encrypted at rest 
using AES-256. Access logs must be retained for 90 days minimum. 
Data classification reviews are required quarterly.
Section 2: Development Standards. All production code must pass 
a minimum of 85% test coverage. Code reviews are mandatory for all commits 
merged into the main branch. Use of deprecated libraries is prohibited.
Section 3: Incident Response Protocol. In the event of a security breach, 
the lead engineer must be notified within 1 hour. A full post-mortem analysis 
is required within 72 hours of incident resolution. Communication protocols 
must follow the defined chain of command.
Section 4: Remote Work Policy. Employees working remotely must use 
company-provided VPN and secure multi-factor authentication (MFA). 
Personal device usage is strictly prohibited for accessing sensitive data.
All remote access must be audited monthly.
"""

VECTOR_STORE_PATH = "./chroma_policy_db"

# 2. Knowledge Base Manager Class
class PolicyKnowledgeBaseManager:
    """
    Manages the ingestion, embedding, persistence, and retrieval 
    for the internal policy documentation using LangChain and ChromaDB.
    """
    def __init__(self, embedding_model, db_path):
        """Initializes the manager, setting up the embedding model and file path."""
        self.embedding_model = embedding_model
        self.db_path = db_path
        self.vector_store = None
        self.policy_file_path = "temp_policy.txt"
        
        # Write mock data to a temporary file for the LangChain TextLoader
        with open(self.policy_file_path, "w") as f:
            f.write(POLICY_TEXT)

    def _load_and_split_documents(self) -> List[Document]:
        """Loads the raw text file and chunks it into manageable, semantically coherent pieces."""
        print("--- 1. Loading and Chunking Documents ---")
        loader = TextLoader(self.policy_file_path)
        documents = loader.load()
        
        # Initialize recursive splitter optimized for structured text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", " "],
            length_function=len,
        )
        
        # Perform the splitting
        split_docs = text_splitter.split_documents(documents)
        print(f"Original text split into {len(split_docs)} chunks.")
        return split_docs

    def create_vector_store(self):
        """Embeds the chunks and persists the resulting vectors to the Chroma vector store."""
        split_docs = self._load_and_split_documents()
        
        # Clean up previous database instance if it exists
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)
            
        print("--- 2. Creating and Persisting Vector Store (Embedding) ---")
        
        # Initialize ChromaDB from the documents and embedding model
        self.vector_store = Chroma.from_documents(
            documents=split_docs,
            embedding=self.embedding_model,
            persist_directory=self.db_path
        )
        
        # Explicitly persist the collection to disk for later use
        self.vector_store.persist()
        print(f"Vector store successfully created and persisted at: {self.db_path}")

    def get_retriever(self, k: int = 3):
        """Configures and returns a standard VectorStoreRetriever object."""
        if self.vector_store is None:
            # If the vector store was not created in this session, load it from disk
            print("Loading existing vector store from disk...")
            self.vector_store = Chroma(
                persist_directory=self.db_path, 
                embedding_function=self.embedding_model
            )
        
        # Convert the vector store object into a LangChain Retriever
        # Using search_kwargs to specify the number of nearest neighbors (k)
        retriever = self.vector_store.as_retriever(search_kwargs={"k": k})
        print(f"--- 3. Retriever Initialized (k={k} neighbors) ---")
        return retriever

    def run_retrieval_query(self, query: str, k: int = 3):
        """Executes the retrieval process: query -> embedding -> search -> documents."""
        retriever = self.get_retriever(k=k)
        
        print(f"\n--- 4. Executing Retrieval for Query: '{query}' ---")
        
        # The 'invoke' method handles the embedding of the query and the similarity search
        retrieved_docs = retriever.invoke(query)
        
        print(f"Successfully retrieved {len(retrieved_docs)} relevant documents:")
        for i, doc in enumerate(retrieved_docs):
            source = doc.metadata.get('source', 'N/A')
            print(f"\n  [Result {i+1}] (Source: {source})")
            print(f"  Content:\n---")
            print(doc.page_content)
            print("---")
        
        return retrieved_docs

    def cleanup(self):
        """Removes temporary files and the persistent database directory."""
        if os.path.exists(self.policy_file_path):
            os.remove(self.policy_file_path)
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)
        print("\nCleanup complete. Temporary files and database removed.")


# 3. Main Execution Block
if __name__ == "__main__":
    
    # Initialize the embedding model (essential for converting text to vectors)
    # We use a robust, small OpenAI model for efficiency.
    try:
        embedding_model = OpenAIEmbeddings(model="text-embedding-3-small") 
    except Exception as e:
        print(f"ERROR: Failed to initialize OpenAIEmbeddings. Is OPENAI_API_KEY set? Details: {e}")
        exit()

    # Initialize the manager
    manager = PolicyKnowledgeBaseManager(embedding_model, VECTOR_STORE_PATH)
    
    try:
        # Step A: Ingestion Pipeline - Create and persist the vector store
        manager.create_vector_store()
        
        # Step B: Retrieval Phase - Define the query
        user_query = "What is the mandatory timeline for reporting a security incident and subsequent analysis?"
        
        # Step C: Run the retrieval, fetching the top 2 most relevant chunks
        results = manager.run_retrieval_query(user_query, k=2)
        
    finally:
        # Ensure cleanup runs even if an error occurs
        manager.cleanup()
