
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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- 1. Setup and Model Definition ---

# Base is the foundational class that links our Python classes 
# (models) to the SQLAlchemy system and the database metadata.
Base = declarative_base()

class Note(Base):
    # __tablename__ is mandatory and tells SQLAlchemy which SQL table 
    # this Python class maps to.
    __tablename__ = 'notes'

    # Define columns using SQLAlchemy's Column objects.
    # Python attribute 'id' maps to the 'id' column (Integer, Primary Key)
    id = Column(Integer, primary_key=True)
    
    # Python attribute 'title' maps to the 'title' column (String up to 100 chars, cannot be NULL)
    title = Column(String(100), nullable=False)
    
    # Python attribute 'content' maps to the 'content' column (flexible String/Text type)
    content = Column(String)

    def __repr__(self):
        # A standard Python method for representing the object clearly when printed
        return f"<Note(id={self.id}, title='{self.title[:25]}...')>"

# --- 2. Database Connection and Setup ---

DB_FILE = 'orm_example.db'
# We remove the file if it exists to ensure a clean run every time
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

# Create the Engine. The Engine is the source of database connectivity.
# 'sqlite:///orm_example.db' is the connection string (dialect://path)
engine = create_engine(f'sqlite:///{DB_FILE}')

# Use the Base metadata to issue CREATE TABLE statements to the database 
# for all defined models (in this case, only the Note class).
Base.metadata.create_all(engine)
print(f"Database tables created successfully in {DB_FILE}")

# --- 3. Session Configuration ---

# Create a configured Session class bound to the engine. 
# This class will be used to instantiate transactional sessions.
Session = sessionmaker(bind=engine)

# --- 4. CRUD Operation: Create (Insert) ---

# Instantiate a session object to begin a unit of work (transaction)
session = Session()

# 4a. Create Python objects. This is the ORM in action!
note_a = Note(title='Project Kickoff', content='Start planning the new API endpoints.')
note_b = Note(title='Grocery List', content='Milk, Bread, Cheese.')

# 4b. Add the objects to the session. They are now "staged" for insertion.
session.add(note_a)
session.add(note_b)

# 4c. Commit the transaction. This executes the SQL INSERT statements.
print("\n--- Inserting Records ---")
session.commit()
print(f"Note A assigned ID: {note_a.id}")
print(f"Note B assigned ID: {note_b.id}")

# --- 5. CRUD Operation: Read (Query) ---

print("\n--- Querying Records ---")

# 5a. Read all records in the table (equivalent to SELECT * FROM notes)
all_notes = session.query(Note).all()
print(f"Total notes found: {len(all_notes)}")
print("List of all notes:")
for note in all_notes:
    # We use the defined __repr__ method here
    print(f"  > {note}")

# 5b. Read a specific record using filtering (equivalent to WHERE clause)
# Find the note whose title is 'Grocery List'
grocery_note = session.query(Note).filter(Note.title == 'Grocery List').first()

if grocery_note:
    print("\nSpecific Query Result (Grocery List):")
    print(f"  Title: {grocery_note.title}")
    print(f"  Content: {grocery_note.content}")
else:
    print("Error: Specific note not found.")

# --- 6. Cleanup ---

# Close the session to release the database connection resource.
session.close()

# Note: We do not need to clean up the DB_FILE here, as we did that at the start.
