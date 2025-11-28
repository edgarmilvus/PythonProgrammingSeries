
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

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
import os

# 1. Configuration and Setup
# Define the database file location (SQLite)
DATABASE_URL = "sqlite:///blog_data.db"
# Initialize the declarative base class for model definitions
Base = declarative_base()

# 2. Model Definitions

class User(Base):
    """
    Represents the 'one' side of the one-to-many relationship (One User has Many Posts).
    """
    __tablename__ = 'users'
    
    # Primary Key: Unique identifier for the user
    id = Column(Integer, primary_key=True)
    # Standard data fields, enforcing uniqueness and non-nullability
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), nullable=False)

    # Relationship Definition: Links User to Post objects
    # 'Post' refers to the class name. 'back_populates' links back to the 'author' attribute in Post.
    # 'cascade' ensures that if a User is deleted, all associated Posts are also deleted.
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Post(Base):
    """
    Represents the 'many' side of the one-to-many relationship.
    """
    __tablename__ = 'posts'
    
    # Primary Key
    id = Column(Integer, primary_key=True)
    # Content fields
    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
    # Timestamp, automatically set to the current time upon creation
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Foreign Key: The actual database column linking to the 'users' table
    # This is the physical link: table_name.column_name
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationship Definition: Links Post back to the User object
    # This allows us to access post.author to get the full User object.
    author = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post(title='{self.title}', author_id={self.author_id})>"

# 3. Database Initialization and Session Setup
# If the file exists, delete it to ensure a fresh run (for demonstration purposes)
db_file = DATABASE_URL.replace("sqlite:///", "")
if os.path.exists(db_file):
     os.remove(db_file)

# Create the engine instance
engine = create_engine(DATABASE_URL, echo=False)
# Create all defined tables in the database
Base.metadata.create_all(engine)

# Configure a Session factory
Session = sessionmaker(bind=engine)

# 4. Core Application Logic Functions

def add_initial_data(session):
    """Adds sample users and posts, demonstrating relationship assignment."""
    print("\n--- 4.1 Adding Initial Data ---")

    # Create new User objects
    alice = User(username="alice_dev", email="alice@example.com")
    bob = User(username="bob_data", email="bob@example.com")

    # Method 1: Add posts directly using the 'posts' relationship attribute (Alice)
    # SQLAlchemy handles setting the author_id FK automatically.
    alice.posts.append(Post(title="Intro to ORMs", content="SQLAlchemy makes life easy."))
    alice.posts.append(Post(title="Modeling Best Practices", content="Always define relationships clearly."))

    # Method 2: Create a post and manually assign the User object (Bob)
    bob_post = Post(title="Data Structures in Python", content="Lists, tuples, dictionaries, oh my!")
    bob_post.author = bob # Assigning the object automatically sets bob_post.author_id

    # Stage the changes
    session.add_all([alice, bob, bob_post])
    # Commit the transaction to write data to the database
    session.commit()
    print(f"Added 2 users and 3 posts successfully.")
    return alice, bob

def retrieve_user_posts(session, username):
    """Queries a user and retrieves all associated posts via the relationship."""
    print(f"\n--- 4.2 Querying Posts for User: {username} ---")

    # Query the User table
    user = session.query(User).filter(User.username == username).first()

    if user:
        print(f"Found User: {user.username} (ID: {user.id})")
        # Accessing user.posts triggers a lazy load query for all associated Post records
        print(f"Total Posts by {user.username}: {len(user.posts)}")
        for post in user.posts:
            print(f"  - Post ID {post.id}: '{post.title}' (Created: {post.timestamp.strftime('%Y-%m-%d')})")
    else:
        print(f"User '{username}' not found.")

def demonstrate_relationship_traversal(session):
    """Demonstrates traversing from the 'many' side (Post) back to the 'one' side (User)."""
    print("\n--- 4.3 Relationship Traversal (Post -> User) ---")

    # Find the first post
    first_post = session.query(Post).first()

    if first_post:
        # Access the author object directly via the 'author' relationship attribute
        # This is efficient ORM traversal, not manual FK lookup.
        author_name = first_post.author.username
        print(f"Post Title: '{first_post.title}'")
        print(f"Retrieved Author via ORM relationship: {author_name}")
        print(f"Author Email: {first_post.author.email}")
    else:
        print("No posts found to demonstrate traversal.")

# 5. Main Execution Block
if __name__ == "__main__":
    with Session() as session:
        # Step 1: Add data and commit
        add_initial_data(session)

        # Step 2: Traverse One-to-Many (User -> Posts)
        retrieve_user_posts(session, "alice_dev")

        # Step 3: Traverse Many-to-One (Post -> User)
        demonstrate_relationship_traversal(session)
