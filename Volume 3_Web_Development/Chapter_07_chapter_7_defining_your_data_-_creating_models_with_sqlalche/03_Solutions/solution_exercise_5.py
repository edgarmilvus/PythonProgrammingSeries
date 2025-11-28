
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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

class Supplier(Base):
    __tablename__ = 'supplier'

    # 1. Define Supplier Model
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    contact_email = Column(String(120), unique=True)
    
    # 3. Establish Relationship (One side)
    products = relationship(
        "Product", 
        backref="supplier", 
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Supplier(name='{self.name}')>"

class Product(Base):
    __tablename__ = 'product'

    # Existing fields (assumed)
    id = Column(Integer, primary_key=True)
    product_name = Column(String(200), nullable=False)
    price = Column(Integer) 

    # 2. Updated Product Requirements
    # SKU: Unique and Non-nullable identifier
    sku = Column(String(50), unique=True, nullable=False)
    stock_quantity = Column(Integer, default=0)
    
    # Foreign Key to Supplier
    supplier_id = Column(Integer, ForeignKey('supplier.id'))

    def __repr__(self):
        return f"<Product(name='{self.product_name}', sku='{self.sku}')>"
