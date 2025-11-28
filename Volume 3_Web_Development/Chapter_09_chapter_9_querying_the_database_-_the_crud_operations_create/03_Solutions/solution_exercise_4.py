
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

# Source File: solution_exercise_4.py
# Description: Solution for Exercise 4
# ==========================================

from flask import Flask, request, jsonify, abort
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

# --- 1. Setup (Assume this is pre-configured) ---
app = Flask(__name__)
# In a real app, this would use configuration files
engine = create_engine('sqlite:///:memory:', echo=False) 
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_name = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author_name": self.author_name
        }

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Helper function to get a new session for the request context
def get_db_session():
    return Session()

# --- 2. Initial Data Population ---
def populate_data():
    session = get_db_session()
    session.add_all([
        Book(id=1, title="The Hitchhiker's Guide", author_name="Douglas Adams"),
        Book(id=2, title="Fluent Python", author_name="Luciano Ramalho")
    ])
    session.commit()
    session.close()

populate_data()

# --- 3. The Interactive Challenge Implementation (Completed Logic) ---
@app.route('/api/v1/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_book_resource(book_id):
    session = get_db_session()
    book = session.get(Book, book_id)
    
    # Check if resource exists first (applies to all methods)
    if book is None:
        session.close()
        # Use Flask's abort to immediately return a standard HTTP error
        abort(404, description=f"Book with ID {book_id} not found.")

    try:
        if request.method == 'GET':
            # Requirement 3: Read Operation
            return jsonify(book.to_dict()), 200

        elif request.method == 'PUT':
            # Requirement 4: Update Operation
            data = request.get_json()
            if not data:
                # 400 Bad Request if no JSON is provided
                abort(400, description="Missing or invalid JSON data.")
            
            # Safely update attributes
            updated = False
            if 'title' in data:
                book.title = data['title']
                updated = True
            if 'author_name' in data:
                book.author_name = data['author_name']
                updated = True
            
            if not updated:
                 # 400 Bad Request if JSON is empty or contains no valid fields
                abort(400, description="No valid fields provided for update.")

            # Commit the change
            session.commit()
            return jsonify(book.to_dict()), 200

        elif request.method == 'DELETE':
            # Requirement 5: Delete Operation
            session.delete(book)
            session.commit()
            # 204 No Content is the standard response for successful deletion
            return '', 204

    except IntegrityError:
        # Requirement 6: Rollback on Database Error (e.g., trying to set title to NULL if it was NOT NULL)
        session.rollback()
        # 409 Conflict is appropriate for constraint violations
        return jsonify({"error": "Database integrity constraint violated."}), 409

    except Exception as e:
        # Catch all other unexpected errors
        session.rollback()
        # In a real app, use app.logger.error(f"...")
        print(f"An unexpected error occurred: {e}") 
        return jsonify({"error": "Internal Server Error"}), 500
        
    finally:
        # Requirement 6: Ensure session is always closed
        session.close()

# Example usage (Test client simulation)
if __name__ == '__main__':
    print("--- Testing CRUD Resource Endpoint ---")
    with app.test_client() as client:
        
        # 1. GET (Read) - Success
        response_get = client.get('/api/v1/books/1')
        print(f"\n[1] GET /api/v1/books/1: Status {response_get.status_code}")
        print(f"    Data: {response_get.get_json()}")
        
        # 2. PUT (Update) - Success
        new_data = {"title": "The Hitchhiker's Guide to the Galaxy (Revised)"}
        response_put = client.put('/api/v1/books/1', json=new_data)
        print(f"\n[2] PUT /api/v1/books/1: Status {response_put.status_code}")
        print(f"    New Title: {response_put.get_json().get('title')}")
        
        # 3. DELETE (Delete) - Success
        response_delete = client.delete('/api/v1/books/2')
        print(f"\n[3] DELETE /api/v1/books/2: Status {response_delete.status_code} (Expected 204 No Content)")
        
        # 4. GET after Delete (Verify 404)
        response_verify = client.get('/api/v1/books/2')
        print(f"\n[4] GET /api/v1/books/2: Status {response_verify.status_code} (Expected 404)")
        
        # 5. GET (Verify 404 for non-existent ID)
        response_404 = client.get('/api/v1/books/999')
        print(f"\n[5] GET /api/v1/books/999: Status {response_404.status_code} (Expected 404)")
