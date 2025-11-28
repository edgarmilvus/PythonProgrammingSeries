
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
from pathlib import Path
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# --- 1. Data Simulation ---
DOCS_DIR = Path("./temp_pyops_docs")
DOCS_DIR.mkdir(exist_ok=True)

docs_content = {
    "doc_1.txt": "# PyOps.async_connect\nFunction: Establishes an asynchronous connection to the primary data warehouse.\nRequired Parameters: host (str), port (int, default 5432), timeout (float).",
    "doc_2.txt": "# PyOps.data_filter\nFunction: Filters large datasets based on dynamic criteria.\nUsage: Recommended for datasets exceeding 1GB. Parameters: dataset (pd.DataFrame), criteria (dict).",
    "doc_3.txt": "# PyOps.schema_validate\nFunction: Validates incoming JSON payloads against a predefined Pydantic schema.\nReturns: Boolean indicating validity. Note: Requires the 'pydantic' library."
}

for filename, content in docs_content.items():
    (DOCS_DIR / filename).write_text(content)

# --- 2. Ingestion and Indexing ---
loader = DirectoryLoader(DOCS_DIR, glob="*.txt")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = Chroma.from_documents(chunks, embeddings, collection_name="pyops_docs")
retriever = vector_store.as_retriever()

# --- 3. Retrieval Chain Construction ---
llm_rag = ChatOpenAI(model="gpt-4o-mini", temperature=0)

template = """
You are a technical documentation assistant. Use ONLY the following context 
to answer the user's question. If the answer is not found in the context, 
state clearly that the information is unavailable in the PyOps documentation.

Context:
{context}

Question: {question}
"""
prompt_rag = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    """Formats retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()}
    | prompt_rag
    | llm_rag
    | StrOutputParser()
)

# --- 4. Testing ---
print("--- RAG Chain Testing ---")

# Test A: Answerable question
q_answerable = "What are the required parameters for PyOps.async_connect?"
print(f"\nQ: {q_answerable}")
a_answerable = rag_chain.invoke(q_answerable)
print(f"A: {a_answerable}")

# Test B: Unanswerable question
q_unanswerable = "What is the capital of France?"
print(f"\nQ: {q_unanswerable}")
a_unanswerable = rag_chain.invoke(q_unanswerable)
print(f"A: {a_unanswerable}")

# Cleanup
shutil.rmtree(DOCS_DIR)
