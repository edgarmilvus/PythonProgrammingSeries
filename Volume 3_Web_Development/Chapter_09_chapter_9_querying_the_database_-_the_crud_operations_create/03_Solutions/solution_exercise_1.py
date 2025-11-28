
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

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

# Configuration and Setup
# Use an in-memory SQLite database for demonstration
engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# 1. Define the Model
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # Define sku as unique
    sku = Column(String, unique=True, nullable=False)
    price = Column(Float)

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', sku='{self.sku}')"

# Create tables
Base.metadata.create_all(engine)

def perform_batch_insertion():
    session = Session()

    # 2. Batch Insertion Data (Intentional duplicate SKU: SKU002)
    product_data = [
        {"name": "Laptop Pro", "sku": "SKU001", "price": 1200.00},
        {"name": "Mouse Wireless", "sku": "SKU002", "price": 25.50},
        {"name": "Keyboard Mechanical", "sku": "SKU003", "price": 95.00},
        # This entry will cause the IntegrityError
        {"name": "Duplicate Mouse", "sku": "SKU002", "price": 10.00},
        {"name": "Monitor 4K", "sku": "SKU004", "price": 450.00},
    ]

    # Convert dictionaries to Product objects
    products_to_add = [Product(**data) for data in product_data]

    print("Attempting batch insertion...")
    session.add_all(products_to_add)

    # 4. Transaction Management and 5. Rollback
    try:
        session.commit()
        print("Batch insertion successful.")
    except IntegrityError as e:
        print("\n--- ERROR DETECTED ---")
        # Rollback the entire transaction due to unique constraint violation
        session.rollback()
        print(f"IntegrityError occurred during commit: {e.orig}")
        print("The entire batch transaction has been rolled back.")
        print("----------------------\n")
    except Exception as e:
        session.rollback()
        print(f"An unexpected error occurred: {e}")
    finally:
        # 6. Verification
        count = session.query(Product).count()
        print(f"Verification: Total products saved in the database: {count}")
        if count > 0:
            print("Saved products:", session.query(Product).all())
        session.close()

perform_batch_insertion()
