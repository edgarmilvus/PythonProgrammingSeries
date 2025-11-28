
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
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Define the Base Class for models
# This foundation class acts as a catalog for all defined models.
Base = declarative_base()

# 2. Define the Model (The User Table Blueprint)
class User(Base):
    # __tablename__: Maps this Python class to a specific table name in the DB
    __tablename__ = 'users'

    # id: The Primary Key column. Ensures uniqueness and indexing.
    id = Column(Integer, primary_key=True)

    # username: A required, unique string field, limited to 50 characters.
    username = Column(String(50), nullable=False, unique=True)

    # email: A required string field, limited to 100 characters.
    email = Column(String(100), nullable=False)

    # A standard representation method for debugging and printing the object
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

# --- Database Setup and Interaction ---

# 3. Setup the Engine (The database connection interface)
# 'sqlite:///:memory:' means we use a temporary database that exists only in RAM.
# echo=True instructs SQLAlchemy to print the raw SQL it generates, which is vital for learning.
engine = create_engine('sqlite:///:memory:', echo=True)

# 4. Create Tables
# Base.metadata contains the structure of all models inheriting from Base.
# create_all translates these structures into SQL and executes the CREATE TABLE commands.
Base.metadata.create_all(engine)

# 5. Setup Session Factory
# A session is the temporary holding zone for changes before they are committed.
Session = sessionmaker(bind=engine)
session = Session()

# 6. Interaction: Creating and Adding Data
print("\n--- Step 6: Adding New User Instance ---")
# Create an instance of our Python User class
new_user = User(username='a_developer', email='dev@example.com')

# Stage the new object in the session (it's waiting to be saved)
session.add(new_user)

# Commit the transaction (writing the staged changes permanently to the database)
session.commit()
print(f"User successfully added and committed: {new_user}")

# 7. Interaction: Querying Data
print("\n--- Step 7: Querying Data ---")
# Query the User model, filter the results, and retrieve the first match.
retrieved_user = session.query(User).filter_by(username='a_developer').first()

print(f"Retrieved user object data: {retrieved_user}")
print(f"Accessing data via object attribute: ID = {retrieved_user.id}")

# 8. Clean up
# Close the session to release resources, concluding the unit of work.
session.close()
