
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
import sys
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- 1. Configuration Constants ---

# Define the database URL. In production, this should always come from 
# an Environment Variable for security and flexibility.
DATABASE_URL = os.environ.get(
    "DB_CONNECTION_STRING", 
    "sqlite:///./alembic_setup_example.db" # Default to a local SQLite file
)

# --- 2. SQLAlchemy Model Definition ---

# Base class for declarative models. This object aggregates all table definitions.
Base = declarative_base()

class User(Base):
    """
    A simple model representing a User table.
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

# --- 3. The Alembic Bridge Setup (The env.py equivalent) ---

# CRITICAL STEP: Alembic needs access to the aggregated metadata object.
# This Base.metadata object holds the blueprint for ALL defined tables.
target_metadata = Base.metadata

def configure_alembic_bridge():
    """
    Simulates the core setup logic found within Alembic's env.py file.
    This function establishes the connection and links the metadata.
    """
    print(f"--- 1. Connecting to Database: {DATABASE_URL} ---")
    
    # Create the engine using the configured URL.
    engine = create_engine(DATABASE_URL)
    
    # Drop and recreate tables for demonstration purposes (simulating a clean start).
    # NOTE: In a real migration scenario, you would NOT do this, as it deletes data.
    target_metadata.drop_all(bind=engine)
    target_metadata.create_all(bind=engine)
    
    print("--- 2. Metadata Aggregation Complete ---")
    
    # Print the aggregated table names to confirm Alembic can see them.
    print("Tables visible to the migration tool (target_metadata):")
    for table_name in target_metadata.tables.keys():
        print(f"  - {table_name}")
        
    print(f"\nConfiguration successful. {len(target_metadata.tables)} model(s) registered.")
    
# --- 4. Execution ---

if __name__ == "__main__":
    configure_alembic_bridge()
