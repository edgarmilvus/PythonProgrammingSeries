
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

# Source File: solution_exercise_1.py
# Description: Solution for Exercise 1
# ==========================================

# Initialize the main data structure
inventory = {}

def add_stock(department: str, product: str, quantity: int, price: float):
    """
    Adds a new product or updates the stock and price of an existing product.
    Creates the department if it does not exist.
    """
    # 1. Check if the department exists, if not, initialize it.
    if department not in inventory:
        inventory[department] = {}
    
    # 2. Check if the product exists within the department.
    if product not in inventory[department]:
        # Initialize product entry if new
        inventory[department][product] = {'stock': 0, 'price': price}
    
    # 3. Update stock (add quantity) and set the latest price
    inventory[department][product]['stock'] += quantity
    inventory[department][product]['price'] = price
    print(f"Updated: {product} in {department}. New stock: {inventory[department][product]['stock']}")


def calculate_department_value(department: str) -> float:
    """
    Calculates the total monetary value of all stock within that department.
    Returns 0.0 if the department is not found.
    """
    if department not in inventory:
        return 0.0
    
    total_value = 0.0
    
    # Iterate over the product dictionaries within the department
    for product_data in inventory[department].values():
        # Calculate (Stock * Price) and add to the running total
        total_value += product_data['stock'] * product_data['price']
        
    return round(total_value, 2)


def find_low_stock(threshold: int) -> list[tuple]:
    """
    Iterates through all departments and products, returning a list of tuples 
    (department, product, stock_level) for items below the threshold.
    """
    low_stock_items = []
    
    # Outer loop: Iterate through departments
    for dept, products in inventory.items():
        # Inner loop: Iterate through products in the current department
        for product, data in products.items():
            if data['stock'] < threshold:
                # Append the required tuple format
                low_stock_items.append((dept, product, data['stock']))
                
    return low_stock_items

# --- Testing 20.4.1 ---
print("--- Inventory System Test ---")
add_stock("Electronics", "Laptop", 10, 1200.00)
add_stock("Electronics", "Mouse", 50, 25.50)
add_stock("Apparel", "T-Shirt", 5, 15.00)
add_stock("Electronics", "Laptop", 2, 1199.99) # Update stock and price

electronics_value = calculate_department_value("Electronics")
apparel_value = calculate_department_value("Apparel")

print(f"\nTotal Electronics Value: ${electronics_value}")
print(f"Total Apparel Value: ${apparel_value}")
print(f"Value of non-existent dept: ${calculate_department_value('Books')}")

low_stock = find_low_stock(15)
print(f"\nItems below stock threshold (15): {low_stock}")
