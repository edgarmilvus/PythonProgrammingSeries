
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

# Constants define the expected structure of the raw data
PRODUCT_ID_LENGTH = 8
DATA_SEPARATOR = ';'
PRICE_PREFIX = '$'
OUTPUT_INDENT = "    " # Used for creating structured, indented output

# --- 1. Raw Data Simulation (Inconsistent structure) ---
RAW_INVENTORY_DATA = [
    "[[LOG:ID001234;Laptop Pro X;1299.99]]",
    "[[LOG:ID005678;Keyboard Mech 3000;85.00]]",
    "[[LOG:ID009012;Mouse Ergonomic;25.50]]",
    "[[LOG:ID003456;Monitor 4K Ultra;450.00]]",
    "[[LOG:ID999999;Cable USB-C 3m;15.00]]",
    "[[LOG:ID000000;Defective Entry;ERROR]]" # Intentional error for error handling simulation
]

# --- 2. String Cleaning Function (Uses Slicing and Concatenation) ---
def clean_raw_data(raw_entry):
    """Removes the fixed-length logging prefix '[[LOG:' and suffix ']]' markers."""
    
    # The prefix '[[LOG:' is 8 characters long. We slice from index 8 onwards.
    # This is an example of positive index slicing.
    cleaned_data = raw_entry[8:] 

    # The suffix ']]' is 2 characters long. 
    # We slice up to the second-to-last character (index -2) to remove the suffix.
    # This is an example of negative index slicing.
    cleaned_data = cleaned_data[:-2] 

    # Return the standardized string
    # Although we don't explicitly use the '+' operator, the sequential slicing 
    # and assignment effectively rebuilds the string structure.
    return cleaned_data

# --- 3. Data Parsing Function (Uses Slicing and Splitting) ---
def parse_product_entry(cleaned_entry):
    """
    Parses the cleaned string into ID, Name, and Price using slicing and separators.
    """
    try:
        # 3a. Extract the fixed-length Product ID using slicing
        # The ID is always the first PRODUCT_ID_LENGTH (8) characters.
        product_id = cleaned_entry[:PRODUCT_ID_LENGTH]

        # 3b. Extract the remaining data string (Name and Price)
        # We start slicing after the ID and the separator (8 characters + 1 separator = index 9)
        data_part = cleaned_entry[PRODUCT_ID_LENGTH + 1:]

        # 3c. Separate Name and Price using the defined separator
        # This uses the string method split() to divide the string into a list of parts
        parts = data_part.split(DATA_SEPARATOR)

        if len(parts) != 2:
            return None, None, None # Invalid format structure

        product_name = parts[0].strip()
        raw_price = parts[1].strip()

        # 3d. Basic validation: Ensure price is numeric before conversion
        # This handles the intentional 'ERROR' entry gracefully
        if not all(c.isdigit() or c == '.' for c in raw_price):
            raise ValueError("Price field contains non-numeric characters.")

        # Convert price to float for accurate formatting later
        price_value = float(raw_price)

        return product_id, product_name, price_value

    except (IndexError, ValueError) as e:
        # Log the error and return None values to signal failure
        print(f"# ERROR: Failed to parse entry '{cleaned_entry}'. Reason: {e}")
        return None, None, None

# --- 4. Formatting Function (Uses F-strings) ---
def format_record(product_id, name, price_value):
    """Formats the parsed data into a standardized, JSON-like string record."""

    # Format the price using an f-string format specifier:
    # :,.2f ensures commas for thousands separation and exactly two decimal places.
    formatted_price = f"{price_value:,.2f}"

    # Use f-strings for dynamic insertion and precise structure creation.
    # We use implicit string concatenation across multiple lines inside parentheses.
    record_string = (
        f"{OUTPUT_INDENT}{{\n"
        f'{OUTPUT_INDENT}{OUTPUT_INDENT}"id": "{product_id}",\n'
        f'{OUTPUT_INDENT}{OUTPUT_INDENT}"name": "{name}",\n'
        f'{OUTPUT_INDENT}{OUTPUT_INDENT}"price": "{PRICE_PREFIX}{formatted_price}"\n'
        f"{OUTPUT_INDENT}}}"
    )
    return record_string

# --- 5. Main Execution Logic ---
def run_serializer(data_list):
    """Iterates through the raw data, processes it, and generates the final output."""
    processed_records = []
    error_count = 0

    print("--- Starting Inventory Serialization Process ---")

    for i, raw_entry in enumerate(data_list):
        print(f"\nProcessing Entry {i+1}: {raw_entry}")

        # Step 1: Clean the raw string (Slicing/Concatenation)
        cleaned_string = clean_raw_data(raw_entry)
        print(f"  -> Cleaned String: {cleaned_string}")

        # Step 2: Parse the components (Slicing/Splitting)
        p_id, p_name, p_price = parse_product_entry(cleaned_string)

        if p_id and p_name and p_price is not None:
            # Step 3: Format the output (F-strings)
            formatted_output = format_record(p_id, p_name, p_price)
            processed_records.append(formatted_output)
            print("  -> SUCCESS: Record formatted.")
        else:
            error_count += 1
            print("  -> FAILURE: Skipping entry due to parsing error.")


    print("\n--- Serialization Complete ---")
    print(f"Total processed records: {len(processed_records)}")
    print(f"Total errors skipped: {error_count}")

    # Final step: Concatenate all individual records together, separated by a comma and newline,
    # and wrap them in list markers ([ and ]). This uses the string method join().
    final_output = "[\n" + ",\n".join(processed_records) + "\n]"
    return final_output

# Execute the main function and print the final structured output
FINAL_REPORT = run_serializer(RAW_INVENTORY_DATA)
print("\n" * 2)
print("=" * 40)
print("FINAL STRUCTURED INVENTORY REPORT")
print("=" * 40)
print(FINAL_REPORT)
