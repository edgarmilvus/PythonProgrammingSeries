
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
from dotenv import load_dotenv
from typing import Tuple
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import Runnable

# --- Configuration and Setup ---

load_dotenv()
# Ensure API key is set for OpenAI components
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable not set. Please configure .env file.")

# 1. Define the proprietary knowledge base (simulating a policy document)
POLICY_TEXT = """
Section A: Employee Travel Policy. All business travel expenses must be pre-approved by a direct manager 
at least 7 days in advance. Reimbursement claims must be submitted within 30 days of the trip's completion. 
The maximum daily allowance for meals is $75 USD, regardless of destination.

Section B: Remote Work Policy. Employees are permitted to work remotely up to three days per week. 
This requires a signed remote work agreement (RWA) filed annually. Employees must maintain a dedicated, 
secure workspace and ensure internet connectivity meets minimum speed requirements (25 Mbps download).

Section C: Intellectual Property Rights. All code, documentation, and creative works produced during 
working hours are the sole property of the company. Any exceptions must be documented in writing 
and signed by the Chief Legal Officer. This clause applies even if the work is performed outside 
of the primary office location.

Section D: Vacation Accrual. Full-time employees accrue 1.5 days of paid vacation per month, 
starting immediately upon hire. Vacation days can only be used after the successful completion 
of the 90-day probationary period.
"""

# --- RAG Pipeline Components ---

def setup_rag_pipeline(policy_content: str) -> Tuple[Runnable, Chroma]:
    """
    Initializes and returns the complete RAG chain using LCEL.
    This function handles ingestion, indexing, retrieval, and generation setup.
    """
    
    # --- Ingestion and Splitting ---
    # We simulate loading content from a persistent document source
    temp_file = "policy_doc.txt"
    with open(temp_file, "w") as f:
        f.write(policy_content)
    
    loader = TextLoader(temp_file)
    documents = loader.load()
    
    # Use RecursiveCharacterTextSplitter for intelligent chunking based on structure
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )
    docs = text_splitter.split_documents(documents)

    # --- Indexing (Vector Store Creation) ---
    # Initialize the embedding model (critical for semantic search)
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # Create a volatile, in-memory Chroma vector store from the chunked documents
    vectorstore = Chroma.from_documents(
        documents=docs, 
        embedding=embedding_model,
        collection_name="corporate_policies_rag"
    )
    
    # --- Retrieval Configuration ---
    # Convert the vector store into a retriever instance
    # search_kwargs={"k": 2} ensures we only pass the top 2 most relevant chunks to the LLM
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # --- Generation Setup (LLM and Prompt) ---
    # Use a modern, cost-effective LLM for the generation step
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    
    # Define the system prompt template, strictly instructing the LLM on grounding
    template = """
    You are an expert HR assistant. Your task is to provide concise, accurate answers 
    based ONLY on the provided context. If the answer requires information not explicitly 
    present in the context, you MUST state that the information is unavailable in the 
    corporate policy documents. Do not use external or general knowledge.

    Context: {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # --- Orchestration: Building the LCEL Chain ---
    
    # 1. Define the context retrieval step. The retriever takes the query, finds documents, 
    #    and returns them as a list of Document objects.
    # 2. RunnablePassthrough is used to pipe the original user question through the chain
    #    so it can be used alongside the context in the final prompt.
    # 3. The input dictionary is constructed: {"context": retrieved_docs, "question": original_query}
    
    rag_chain = (
        {
            "context": retriever, 
            "question": RunnablePassthrough() 
        }
        | prompt # Format the input dictionary into a complete prompt
        | llm    # Send the prompt to the LLM for generation
        | StrOutputParser() # Extract the final string response
    )
    
    # Clean up the temporary file used for loading
    os.remove(temp_file)
    
    return rag_chain, vectorstore

# --- Execution ---

if __name__ == "__main__":
    print("--- RAG Pipeline Initialization ---")
    
    # Setup the chain and get the vector store reference for clean up
    rag_chain, vectorstore = setup_rag_pipeline(POLICY_TEXT)
    
    # --- Test 1: Grounded Query ---
    query_1 = "How many days of remote work are permitted per week, and what is the minimum required internet speed?"
    print(f"\n[Query 1]: {query_1}")
    
    # Invoke the chain synchronously
    response_1 = rag_chain.invoke(query_1)
    print(f"\n[Response 1 (Grounded)]:\n{response_1}")

    # --- Test 2: Ungrounded Query (Testing Hallucination Prevention) ---
    query_2 = "What is the policy regarding sick leave for employees who have been with the company for less than six months?"
    print(f"\n[Query 2]: {query_2}")
    
    # Invoke the chain
    response_2 = rag_chain.invoke(query_2)
    print(f"\n[Response 2 (Ungrounded)]:\n{response_2}")
    
    # --- Test 3: Specific Detail Query ---
    query_3 = "When does vacation day accrual begin, and when can the days actually be used?"
    print(f"\n[Query 3]: {query_3}")
    
    response_3 = rag_chain.invoke(query_3)
    print(f"\n[Response 3 (Grounded Detail)]:\n{response_3}")
    
    # Cleanup the in-memory vector store collection
    vectorstore.delete_collection()
    print("\n--- RAG Pipeline Complete and Resources Cleaned Up ---")
