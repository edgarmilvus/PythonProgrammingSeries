
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
from google import genai
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Literal

# --- 1. Pydantic Schema Definitions ---

# Define the smallest unit: a single item on the receipt/invoice
class LineItem(BaseModel):
    """Represents a single item purchased on the financial document."""
    description: str = Field(description="A brief description of the item purchased.")
    quantity: int = Field(description="The number of units purchased (must be an integer).")
    unit_price: float = Field(description="The cost of a single unit.")
    line_total: float = Field(description="The total cost for this line item (quantity * unit_price).")

# Define conditional details for specific categories (e.g., Travel)
class TravelDetails(BaseModel):
    """Details required if the expense is categorized as Business Travel."""
    destination_city: str = Field(description="The primary destination city of the trip.")
    trip_purpose: str = Field(description="A brief summary of the business purpose for the travel.")
    
# Define the expense classification structure
class ExpenseClassification(BaseModel):
    """Defines the category and required metadata for the expense."""
    
    # Use Literal to force the model to select from predefined, strict categories
    category: Literal[
        "Software_Subscription", 
        "Office_Supplies", 
        "Business_Travel", 
        "Marketing_Ad", 
        "Uncategorized"
    ] = Field(description="The primary business category for this expense.")
    
    budget_code: Optional[str] = Field(
        None, 
        description="Internal budget code (e.g., 'BGT-401'). Required for Software and Marketing."
    )
    
    # Use Optional and nested model for conditional data
    travel_info: Optional[TravelDetails] = Field(
        None, 
        description="Detailed travel information, required only if category is 'Business_Travel'."
    )

# Define the main structure for the extracted financial document
class FinancialDocument(BaseModel):
    """The root schema for the extracted and structured financial data."""
    vendor_name: str = Field(description="The legal name of the vendor or service provider.")
    document_id: str = Field(description="The unique invoice or receipt number.")
    
    # Enforce a specific date format for easy database ingestion
    date_issued: str = Field(description="The date the document was issued, formatted strictly as YYYY-MM-DD.")
    
    grand_total: float = Field(description="The final total amount paid, including tax.")
    
    # Restrict currency to supported types
    currency: Literal["USD", "EUR", "GBP"]
    
    # Use the nested LineItem model for the list of purchased goods/services
    items: List[LineItem]
    
    # Include the classification structure
    classification: ExpenseClassification

# --- 2. Unstructured Input Data ---

UNSTRUCTURED_RECEIPT_TEXT = """
Vendor: CloudCompute Solutions LLC
Invoice Number: INV-8734-2024-Q3
Date: 2024/09/15
Total Paid: $1,499.99 USD
Notes: This was a necessary expense for our Q4 product launch planning.
Items:
1. Advanced Data Analysis Suite Subscription: 1 unit @ $999.99 each. Total: $999.99
2. Premium Support Package (1 year): 1 unit @ $500.00 each. Total: $500.00
Tax/Fees: $0.01 (rounding adjustment).
Please categorize this under our core infrastructure budget (Code: INFRA-A1).
"""

# --- 3. API Client Setup ---

try:
    # Initialize the client. Assumes GEMINI_API_KEY is set in environment variables.
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set correctly.")
    exit()

# --- 4. Prompt Construction ---

system_prompt = (
    "You are an expert financial data extraction bot. Your task is to analyze the "
    "provided unstructured receipt text and extract all relevant data points into "
    "a strictly enforced JSON format based on the provided schema. Ensure all "
    "numeric types (float, int) are correctly parsed and that the final output "
    "is a single, valid JSON object matching the FinancialDocument schema."
)

# --- 5. API Call and Structured Output Configuration ---

print("--- Starting Gemini Structured Extraction ---")

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # A fast model suitable for structured extraction
        contents=[system_prompt, UNSTRUCTURED_RECEIPT_TEXT],
        config={
            # CRITICAL: Enforce JSON MIME type
            "response_mime_type": "application/json",
            
            # CRITICAL: Pass the Pydantic schema compiled to JSON Schema format
            "response_json_schema": FinancialDocument.model_json_schema(),
        },
    )

    # --- 6. Post-Processing and Validation ---

    # The response.text is guaranteed to be a syntactically valid JSON string.
    # We use Pydantic's built-in validation to parse the string into a type-safe object.
    extracted_document = FinancialDocument.model_validate_json(response.text)

    print("\n--- Extraction Successful ---")
    print(f"Vendor: {extracted_document.vendor_name}")
    print(f"ID: {extracted_document.document_id}")
    print(f"Total: {extracted_document.currency} {extracted_document.grand_total:.2f}")
    print("-" * 30)

    # Display Classification Details
    classification = extracted_document.classification
    print(f"CLASSIFICATION: {classification.category}")
    print(f"Budget Code: {classification.budget_code if classification.budget_code else 'N/A'}")

    # Display Line Items
    print("\n--- Line Items ---")
    for item in extracted_document.items:
        print(f"  - {item.description} | Qty: {item.quantity} | Unit Price: {item.unit_price:.2f} | Total: {item.line_total:.2f}")

    # Display the raw, validated Pydantic object (for inspection)
    print("\n--- Raw Pydantic Object (JSON Dump) ---")
    print(json.dumps(extracted_document.model_dump(), indent=4))

except ValidationError as e:
    print(f"\n[ERROR] Pydantic Validation Failed after extraction: {e}")
except Exception as e:
    print(f"\n[ERROR] An API or processing error occurred: {e}")

