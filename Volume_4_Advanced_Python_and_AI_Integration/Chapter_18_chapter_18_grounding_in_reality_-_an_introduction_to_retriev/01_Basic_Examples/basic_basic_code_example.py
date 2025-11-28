
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
from dotenv import load_dotenv

# LangChain Core Components
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

# Indexing Components
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma

# Chain Components (LCEL - LangChain Expression Language)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# --- 1. SETUP AND CONFIGURATION ---
# Loads necessary API keys (like OPENAI_API_KEY) from a .env file
load_dotenv() 

# Define the LLM model to be used for generation
LLM_MODEL = "gpt-3.5-turbo-0125"

# --- 2. DATA PREPARATION (The Knowledge Base) ---
# We simulate loading raw documents about advanced Python features and RAG itself.
# These documents represent our external, verifiable knowledge.
raw_documents = [
    Document(
        page_content="Asyncio allows concurrent execution using a single thread, primarily through cooperative multitasking. It relies heavily on the 'await' and 'async' keywords, which define coroutines.",
        metadata={"source": "Python Advanced Guide", "page": 15}
    ),
    Document(
        page_content="Decorators are functions that wrap other functions, modifying their behavior without permanently altering them. They are syntactic sugar using the '@' symbol.",
        metadata={"source": "Python Advanced Guide", "page": 22}
    ),
    Document(
        page_content="The primary goal of RAG is to ensure LLM responses are grounded in verifiable, external knowledge, overcoming inherent knowledge cutoff limitations.",
        metadata={"source": "AI Integration Handbook", "page": 5}
    )
]

# --- 3. INDEXING: Splitting, Embedding, and Storing ---
# This phase converts human-readable text into machine-searchable vectors.

# 3a. Splitting (Chunking large documents into smaller, searchable pieces)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20 # Overlap helps maintain context across chunks
)
split_docs = text_splitter.split_documents(raw_documents)

# 3b. Defining the Embedding Model
# This model translates text chunks into high-dimensional numerical vectors.
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# 3c. Storing the Vectors in a Vector Database (Chroma is used for simplicity)
# Chroma performs the embedding calculation and stores the resulting vectors,
# making them available for rapid semantic search.
vector_store = Chroma.from_documents(
    documents=split_docs,
    embedding=embedding_model,
    collection_name="rag_intro_data"
)

# --- 4. RETRIEVAL: Creating the Search Interface ---

# The retriever is the interface that abstracts the search logic from the vector store.
# search_kwargs={"k": 2} specifies that we want the top 2 most semantically similar chunks.
retriever = vector_store.as_retriever(search_kwargs={"k": 2}) 

# --- 5. AUGMENTATION: Defining the Prompt and Chain ---

# 5a. Define the Prompt Template (The critical RAG component)
# The prompt explicitly defines two placeholders: {context} for retrieved data 
# and {input} for the user query.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert Python developer assistant. Answer the user's question based ONLY on the provided context. If the answer is not in the context, state that you cannot find the information."),
    ("user", "Context: {context}\n\nQuestion: {input}")
])

# 5b. Define the LLM
llm = ChatOpenAI(model=LLM_MODEL, temperature=0.0)

# 5c. Define the Document Combining Chain (Stuffing Mechanism)
# This chain takes the list of retrieved documents and "stuffs" them 
# into the single {context} variable defined in the prompt.
document_chain = create_stuff_documents_chain(llm, prompt)

# 5d. Define the Full Retrieval Chain (The Orchestrator)
# This chain links the retriever (search) and the document_chain (generation).
# Flow: Retriever -> Document Chain -> LLM
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# --- 6. EXECUTION ---
user_query = "What is the primary function of RAG architecture, and what keywords are essential for Asyncio?"

print(f"--- Running RAG Chain for Query: '{user_query}' ---")
response = retrieval_chain.invoke({"input": user_query})

# --- 7. OUTPUT INSPECTION ---
print("\n[Generated Answer]")
print(response["answer"])

print("\n[Retrieved Context (Source Documents)]")
# The 'context' key holds the documents found by the retriever, proving the grounding.
for doc in response["context"]:
    print(f"Source: {doc.metadata['source']} (Page {doc.metadata['page']}) | Content: {doc.page_content[:50]}...")
