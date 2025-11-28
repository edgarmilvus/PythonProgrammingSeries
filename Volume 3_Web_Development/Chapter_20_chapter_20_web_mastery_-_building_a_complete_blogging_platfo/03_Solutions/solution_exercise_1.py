
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
from datetime import datetime

from flask import Flask, jsonify, request, abort, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

# --- Configuration and Initialization ---

# Define the database path (in-memory SQLite for simplicity)
basedir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = 'sqlite:///' + os.path.join(basedir, 'blog_api.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key-for-blogging-platform'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600 # 1 hour

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Blueprints
user_bp = Blueprint('users', __name__, url_prefix='/api/users')
post_bp = Blueprint('posts', __name__, url_prefix='/api/posts')
tag_bp = Blueprint('tags', __name__, url_prefix='/api/tags') # For Exercise 4

# --- Custom Exception (Exercise 5) ---

class ValidationException(Exception):
    """Custom exception for proactive input validation errors."""
    def __init__(self, messages, status_code=400):
        self.messages = messages
        self.status_code = status_code

@app.errorhandler(ValidationException)
def handle_validation_error(e):
    """Centralized handler for ValidationException (Exercise 5)."""
    response = jsonify({
        "status": e.status_code,
        "error": "Bad Request",
        "messages": e.messages
    })
    response.status_code = e.status_code
    return response

# --- Models (Updated for Exercise 4: Tags) ---

# Exercise 4: Association Table for Many-to-Many
post_tag_association = db.Table('post_tag_association',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Relationship: User has many Posts
    posts = db.relationship('Post', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Key
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Exercise 4: Many-to-Many relationship with Tag
    tags = db.relationship(
        'Tag', secondary=post_tag_association, lazy='subquery',
        backref=db.backref('posts', lazy=True)
    )

class Tag(db.Model):
    # Exercise 4: Tag Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# --- Schemas (Updated for Exercise 1 & 4) ---

class TagSchema(ma.SQLAlchemySchema):
    # Exercise 4: Schema for Tag
    class Meta:
        model = Tag
        fields = ('name',)

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ('id', 'username', 'password_hash') # password_hash included for internal use only

class SanitizedUserSchema(UserSchema):
    # Exercise 1: Inherits from UserSchema but excludes sensitive data
    class Meta:
        model = User
        fields = ('id', 'username') # Explicitly exclude password_hash

class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Post
        load_instance = True
        fields = ('id', 'title', 'body', 'created_at', 'author_id', 'author', 'tags')
    
    # Exercise 4: Serialize tags as a list of names
    tags = ma.List(ma.fields.String(), attribute='tags', dump_only=True)
    
    # Exercise 1: Nested Author serialization (using the full UserSchema for internal/standard use)
    author = ma.Nested(UserSchema, exclude=('password_hash',))

class PostWithSanitizedAuthorSchema(PostSchema):
    # Exercise 1: Use the sanitized schema for the author object
    author = ma.Nested(SanitizedUserSchema)

# Schema Instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)
post_schema = PostSchema()
posts_schema = PostSchema(many=True)
sanitized_posts_schema = PostWithSanitizedAuthorSchema(many=True)

# --- Helper Functions (Exercise 4 & 5) ---

def handle_tags(tag_names):
    """Exercise 4: Processes a list of tag names, creating new Tags if needed."""
    tag_objects = []
    if not tag_names:
        return []
        
    for name in tag_names:
        tag = db.session.execute(db.select(Tag).filter_by(name=name)).scalar_one_or_none()
        if not tag:
            tag = Tag(name=name)
            db.session.add(tag)
            # We don't commit here, we let the post commit handle it.
        tag_objects.append(tag)
    return tag_objects

def validate_post_data(data):
    """Exercise 5: Proactive validation for post creation/update."""
    errors = {}
    title = data.get('title')
    body = data.get('body')

    if not title:
        errors['title'] = 'Title is required.'
    elif len(title) < 5:
        errors['title'] = 'Title must be at least 5 characters long.'

    if not body:
        errors['body'] = 'Body content is required.'

    if errors:
        raise ValidationException(errors)
    
    return data

def validate_user_data(data):
    """Exercise 5: Proactive validation for user registration."""
    errors = {}
    username = data.get('username')
    password = data.get('password')

    if not username:
        errors['username'] = 'Username is required.'
    elif len(username) < 4:
        errors['username'] = 'Username must be at least 4 characters long.'
    
    # Check for existing user proactively
    existing_user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
    if existing_user:
        errors['username'] = 'This username is already taken.'

    if not password:
        errors['password'] = 'Password is required.'
    elif len(password) < 6:
        errors['password'] = 'Password must be at least 6 characters long.'

    if errors:
        raise ValidationException(errors)
    
    return data

# --- Auth Endpoint (Standard Setup) ---

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    
    return jsonify({"msg": "Bad username or password"}), 401

# --- User Blueprint Endpoints ---

@user_bp.route('/', methods=['POST'])
def register_user():
    # Exercise 5: Use proactive validation
    data = request.get_json()
    validate_user_data(data) # Raises ValidationException on failure

    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    return user_schema.dump(new_user), 201

# Exercise 1: Advanced Data Retrieval and Relationship Filtering
@user_bp.route('/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """Retrieves all posts by a specific user, using sanitized serialization."""
    
    # Efficiently load the user and their posts, or 404 if user doesn't exist
    user = db.session.get(User, user_id)
    if user is None:
        abort(404, description=f"User ID {user_id} not found.")

    # Access the posts via the relationship defined in the User model
    posts = user.posts
    
    # Use the specialized schema to ensure the author object is sanitized
    return jsonify(sanitized_posts_schema.dump(posts)), 200

# --- Post Blueprint Endpoints ---

@post_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    # Exercise 5: Use proactive post validation
    validate_post_data(data)

    new_post = Post(
        title=data['title'],
        body=data['body'],
        author_id=current_user_id
    )
    
    # Exercise 4: Handle Tags
    tag_names = data.get('tags', [])
    new_post.tags = handle_tags(tag_names)
    
    db.session.add(new_post)
    db.session.commit()
    
    return post_schema.dump(new_post), 201

# Exercise 3: Implementing Robust Pagination (Refactoring GET /api/posts)
@post_bp.route('/', methods=['GET'])
def list_posts():
    """Retrieves all posts with mandatory pagination."""
    
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
    except ValueError:
        abort(400, description="Page and per_page parameters must be integers.")

    # Enforce limits
    per_page = min(per_page, 50)
    if page < 1 or per_page < 1:
        abort(400, description="Page and per_page must be positive integers.")

    # 3. Database Pagination
    select_stmt = db.select(Post).order_by(Post.created_at.desc())
    
    pagination = db.paginate(
        select_stmt, 
        page=page, 
        per_page=per_page, 
        error_out=False
    )

    # Helper function to generate URLs
    def make_pagination_url(p):
        if p is None: return None
        return url_for('posts.list_posts', page=p, per_page=per_page, _external=True)

    # 4. Metadata Inclusion
    pagination_data = {
        "total_items": pagination.total,
        "total_pages": pagination.pages,
        "current_page": pagination.page,
        "per_page": pagination.per_page,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "next_url": make_pagination_url(pagination.next_num),
        "prev_url": make_pagination_url(pagination.prev_num)
    }

    # 5. Serialization
    return jsonify({
        "pagination": pagination_data,
        "posts": posts_schema.dump(pagination.items)
    }), 200

@post_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = db.session.get_or_404(Post, post_id)
    return post_schema.dump(post)

@post_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    current_user_id = get_jwt_identity()
    post = db.session.get_or_404(Post, post_id)
    data = request.get_json()

    # Exercise 2: Content Ownership Enforcement
    if post.author_id != current_user_id:
        # 4. Forbidden Response
        abort(403, description="You do not have permission to modify this post.")
        
    # Exercise 5: Proactive validation
    validate_post_data(data)

    post.title = data.get('title', post.title)
    post.body = data.get('body', post.body)
    
    # Exercise 4: Handle Tags during update
    if 'tags' in data:
        post.tags = handle_tags(data['tags'])

    db.session.commit()
    return post_schema.dump(post), 200

@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id = get_jwt_identity()
    post = db.session.get_or_404(Post, post_id)

    # Exercise 2: Content Ownership Enforcement
    if post.author_id != current_user_id:
        # 4. Forbidden Response
        abort(403, description="You do not have permission to delete this post.")

    db.session.delete(post)
    db.session.commit()
    return '', 204

# --- Tag Blueprint Endpoints (Exercise 4) ---

@tag_bp.route('/<string:tag_name>/posts', methods=['GET'])
def get_posts_by_tag(tag_name):
    """Exercise 4: Retrieves all posts associated with a specific tag, with pagination."""
    
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
    except ValueError:
        abort(400, description="Page and per_page parameters must be integers.")

    per_page = min(per_page, 50)
    if page < 1 or per_page < 1:
        abort(400, description="Page and per_page must be positive integers.")

    # Query for the tag first
    tag = db.session.execute(db.select(Tag).filter(func.lower(Tag.name) == func.lower(tag_name))).scalar_one_or_none()
    
    if tag is None:
        abort(404, description=f"Tag '{tag_name}' not found.")

    # Efficiently query posts linked to this tag
    select_stmt = db.select(Post).join(Post.tags).filter(Tag.id == tag.id).order_by(Post.created_at.desc())
    
    pagination = db.paginate(
        select_stmt, 
        page=page, 
        per_page=per_page, 
        error_out=False
    )

    # Helper function to generate URLs for this specific tag endpoint
    def make_tag_pagination_url(p):
        if p is None: return None
        return url_for('tags.get_posts_by_tag', tag_name=tag_name, page=p, per_page=per_page, _external=True)

    pagination_data = {
        "total_items": pagination.total,
        "total_pages": pagination.pages,
        "current_page": pagination.page,
        "per_page": pagination.per_page,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "next_url": make_tag_pagination_url(pagination.next_num),
        "prev_url": make_tag_pagination_url(pagination.prev_num)
    }

    return jsonify({
        "tag_name": tag.name,
        "pagination": pagination_data,
        "posts": posts_schema.dump(pagination.items)
    }), 200


# --- Application Setup and Run ---

app.register_blueprint(user_bp)
app.register_blueprint(post_bp)
app.register_blueprint(tag_bp)

@app.cli.command("init-db")
def init_db():
    """Initializes the database and creates tables."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database initialized and tables created.")

if __name__ == '__main__':
    # To run this script:
    # 1. Initialize DB: flask init-db
    # 2. Run app: python app.py
    app.run(debug=True)
