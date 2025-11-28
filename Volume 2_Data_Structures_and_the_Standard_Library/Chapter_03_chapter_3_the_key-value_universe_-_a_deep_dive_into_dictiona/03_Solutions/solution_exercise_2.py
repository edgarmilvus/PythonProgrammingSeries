
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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

# --- Exercise 1 Solution ---

def update_stock(inventory, sku, quantity_change):
    """
    Updates the stock level for a given SKU.
    Uses .get() to safely retrieve the product dictionary.
    """
    # Use .get() to retrieve the product dictionary. If SKU is missing, it returns None.
    product = inventory.get(sku)

    if product:
        # If the product exists, update the stock count.
        product["stock"] += quantity_change
        print(f"Updated stock for {sku}. New stock: {product['stock']}")
        return True
    else:
        print(f"SKU {sku} not found. Stock update failed.")
        return False


def add_new_product(inventory, sku, name, price, initial_stock=0):
    """
    Adds a new product only if the SKU does not already exist.
    Uses .setdefault() for atomic check and insertion.
    """
    new_product_details = {
        "name": name,
        "stock": initial_stock,
        "price": price
    }

    # setdefault() returns the value associated with the key.
    # If the key exists, it returns the existing value (product details).
    # If the key does not exist, it inserts new_product_details and returns it.
    existing_or_new = inventory.setdefault(sku, new_product_details)

    if existing_or_new is new_product_details:
        print(f"Successfully added new product: {name}")
        return new_product_details
    else:
        print(f"SKU {sku} already exists. Addition prevented.")
        return existing_or_new


def get_product_price(inventory, sku):
    """
    Returns the price of a product, or 0.00 if the SKU is missing.
    Uses nested .get() calls for robust default handling.
    """
    # 1. Get the product dictionary (defaulting to an empty dict if SKU is missing)
    product = inventory.get(sku, {})
    
    # 2. Get the price from the product dictionary (defaulting to 0.00 if price key is missing)
    price = product.get("price", 0.00)
    
    return price

# --- Testing Exercise 1 ---
print("\n--- Testing Exercise 1 ---")
inventory_copy = INVENTORY_DATA.copy() # Use a copy for testing

# Test 1.1: Update existing stock
update_stock(inventory_copy, "SKU-4815", -2)

# Test 1.2: Update non-existent SKU
update_stock(inventory_copy, "SKU-9999", 10)

# Test 1.3: Add new product
new_prod = add_new_product(inventory_copy, "SKU-7777", "Mouse Wireless", 45.00, 50)
print(f"Result of new addition: {new_prod}")

# Test 1.4: Attempt to overwrite existing product
existing_prod = add_new_product(inventory_copy, "SKU-4815", "Attempted Overwrite", 1.00)
print(f"Result of overwrite attempt (should be original data): {existing_prod['name']}")

# Test 1.5: Get price for existing and missing product
print(f"Price of SKU-1623: ${get_product_price(inventory_copy, 'SKU-1623'):.2f}")
print(f"Price of SKU-0000 (missing): ${get_product_price(inventory_copy, 'SKU-0000'):.2f}")
