
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

import os
import json
from datetime import timedelta
from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

# --- 1. Initialization and Configuration ---
app = Flask(__name__)

# Configure SQLAlchemy (using in-memory SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure JWT (Use a real secret key in production!)
app.config["JWT_SECRET_KEY"] = "super-secret-key-book-3-chapter-20"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

# --- 2. Database Models ---
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # Define relationship with Post
    posts = db.relationship('Post', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # Foreign Key linking Post to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.user_id,
            'author_username': self.author.username
        }

# --- 3. Authentication Blueprint (auth_bp) ---
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 409

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # Create token, using user.id as the identity payload
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Bad username or password"}), 401

# --- 4. Posts Blueprint (posts_bp) ---
posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/', methods=['GET'])
def get_all_posts():
    # Public endpoint: Anyone can view posts
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts]), 200

@posts_bp.route('/', methods=['POST'])
@jwt_required() # Requires a valid JWT to access
def create_post():
    # Get the authenticated user's ID from the JWT payload
    current_user_id = get_jwt_identity()
    data = request.get_json()

    new_post = Post(
        title=data.get('title'),
        content=data.get('content'),
        user_id=current_user_id # Assign ownership
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post.to_dict()), 201

@posts_bp.route('/<int:post_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def manage_post(post_id):
    current_user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)

    # CRITICAL: Authorization check (ownership enforcement)
    if post.user_id != current_user_id:
        return jsonify({"msg": "Unauthorized: You do not own this post"}), 403

    if request.method == 'PUT':
        data = request.get_json()
        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)
        db.session.commit()
        return jsonify(post.to_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(post)
        db.session.commit()
        return jsonify({"msg": "Post deleted"}), 200

# --- 5. Application Setup and Run ---
app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)

# Setup function to initialize the database and create a test user
@app.before_first_request
def create_tables():
    db.create_all()
    # Create a default user for testing
    if not User.query.filter_by(username='testuser').first():
        test_user = User(username='testuser')
        test_user.set_password('password123')
        db.session.add(test_user)
        db.session.commit()
        print("Database initialized and 'testuser' created.")

if __name__ == '__main__':
    # This setup is for demonstration; use a proper WSGI server in production
    with app.app_context():
        create_tables()
    # app.run(debug=True) # Commented out to prevent execution during documentation
    print("Application setup complete. Endpoints ready.")
