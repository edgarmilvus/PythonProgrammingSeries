
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
import json
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError

# --- 1. Configuration and Setup ---

# Ensure your GEMINI_API_KEY is set in your environment variables
try:
    # Initialize the client
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set correctly.")
    exit()

# Using a powerful model suitable for complex logical reasoning
MODEL_NAME = 'gemini-2.5-flash' # Good balance of speed and reasoning

# --- 2. Defining Context and Rules ---

# Complex business rules for Anti-Money Laundering (AML) compliance
# Note: Rule 3 uses implicit chained comparison logic (500 <= amount <= 1000)
AML_RULES_CONTEXT = """
# AML Compliance Rules (Rule ID: Description)
R101: Any single transaction amount exceeding $5000 USD is automatically flagged as High Risk.
R102: Transactions containing the keywords 'crypto', 'offshore', or 'shell' in the description AND having an amount greater than $1000 USD are flagged as Moderate Risk.
R103: Transactions where the amount is between $500 and $1000 (inclusive) AND the recipient name is 'ShellCorp Holdings' are flagged as Suspicious.
R104: All other transactions are considered Approved.
"""

# Test cases designed to hit different rules
TRANSACTIONS = [
    {"id": "T001", "amount": 6200, "recipient": "Retail Store LLC", "description": "Purchase of equipment."}, # Triggers R101
    {"id": "T002", "amount": 1500, "recipient": "Digital Assets Group", "description": "Transfer for crypto investment."}, # Triggers R102
    {"id": "T003", "amount": 750, "recipient": "ShellCorp Holdings", "description": "Consulting fee."}, # Triggers R103
    {"id": "T004", "amount": 300, "recipient": "Utility Services", "description": "Monthly bill payment."}, # Triggers R104 (Approved)
]

# --- 3. Prompting Strategy 1: Explicit Chain of Thought (CoT) ---

def run_cot_analysis(transaction: dict) -> dict:
    """
    Runs the analysis using CoT prompting. Forces the model to show its work.
    """
    print(f"\n--- Running CoT Analysis for {transaction['id']} ---")
    
    # Construct the transaction description for the prompt
    tx_details = f"Transaction ID: {transaction['id']}, Amount: ${transaction['amount']}, Recipient: {transaction['recipient']}, Description: {transaction['description']}"

    # The CoT prompt mandates explicit, step-by-step verification against the rules.
    cot_prompt = f"""
    You are a Senior AML Compliance Auditor. Your task is to analyze the following transaction against the provided AML Rules Context.

    **AML Rules Context:**
    {AML_RULES_CONTEXT}
    
    **Transaction Details:**
    {tx_details}

    **INSTRUCTION:**
    1. Analyze the transaction against each rule (R101, R102, R103, R104) sequentially.
    2. For each rule, state clearly whether it is 'TRIGGERED' or 'NOT TRIGGERED' and provide a brief justification.
    3. State the final classification (High Risk, Moderate Risk, Suspicious, or Approved).
    4. Provide the ID of the *first* rule that was triggered. If none were triggered, use R104.
    
    **REQUIRED OUTPUT FORMAT (Step-by-step):**
    
    ## Rule Check R101: 
    [Justification for R101]
    
    ## Rule Check R102:
    [Justification for R102]
    
    ... (Continue for all rules)

    --- FINAL VERDICT ---
    Classification: [Classification]
    Triggered Rule ID: [Rule ID]
    """

    start_time = time.time()
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=cot_prompt,
            config=types.GenerateContentConfig(
                temperature=0.2, # Lower temperature for deterministic reasoning
                max_output_tokens=800
            )
        )
        latency = time.time() - start_time
        
        # Simple parsing to extract the final verdict for comparison
        verdict = {
            "latency": f"{latency:.4f}s",
            "classification": "N/A",
            "rule_id": "N/A",
            "full_output": response.text.strip()
        }
        
        # Attempt to extract structured data from the lengthy text output
        for line in response.text.split('\n'):
            if line.startswith("Classification:"):
                verdict['classification'] = line.split(":", 1)[1].strip()
            if line.startswith("Triggered Rule ID:"):
                verdict['rule_id'] = line.split(":", 1)[1].strip()
        
        return verdict
        
    except APIError as e:
        print(f"API Error during CoT analysis: {e}")
        return {"latency": "Error", "classification": "Error", "rule_id": "Error", "full_output": str(e)}

# --- 4. Prompting Strategy 2: Native Reasoning (Zero-Shot CoT) ---

def run_native_analysis(transaction: dict) -> dict:
    """
    Runs the analysis using Native Reasoning/Zero-Shot CoT. 
    Relies on strict output formatting (JSON) and few-shot examples.
    """
    print(f"\n--- Running Native Reasoning Analysis for {transaction['id']} ---")
    
    # Construct the transaction description for the prompt
    tx_details = f"Amount: ${transaction['amount']}, Recipient: {transaction['recipient']}, Description: {transaction['description']}"

    # The Native Reasoning prompt uses few-shot examples and a JSON prefix/suffix 
    # to enforce immediate structured output without explicit step-by-step reasoning.
    native_prompt = f"""
    You are an extremely efficient AML Rule Engine. Based on the provided AML Rules Context, classify the transaction immediately.

    **AML Rules Context:**
    {AML_RULES_CONTEXT}
    
    **INSTRUCTION:**
    Determine the classification and the ID of the rule triggered. Output the result STRICTLY as a JSON object.

    **Example 1 (Few-Shot):**
    Transaction: Amount: $4500, Recipient: Foreign Exchange, Description: Standard wire transfer.
    Output:
    