
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

# app.py: Project Showcase using Template Inheritance

import os
from flask import Flask, render_template, abort

# --- 1. Application Setup ---
# Initialize Flask app. The 'templates' folder is assumed to exist 
# in the same directory as this script.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_key'

# --- 2. Mock Data Source (The model layer) ---
PROJECT_DATA = [
    {'slug': 'project-aurora', 'name': 'Project Aurora', 'status': 'Completed',
     'description': 'A high-performance asynchronous data pipeline written in Python.',
     'tech_stack': ['Python', 'AsyncIO', 'PostgreSQL']},
    {'slug': 'template-master', 'name': 'Template Master', 'status': 'In Progress',
     'description': 'A Flask application demonstrating advanced template inheritance.',
     'tech_stack': ['Flask', 'Jinja2', 'HTML5']},
    {'slug': 'ai-rag-system', 'name': 'AI RAG System', 'status': 'Planning',
     'description': 'Implementing a Retrieval-Augmented Generation system using vector stores.',
     'tech_stack': ['Python', 'LLMs', 'Vector DB', 'RAG']},
]

# --- 3. Utility Function (Data retrieval) ---
def get_project_by_slug(slug):
    """Searches the mock database for a project matching the given URL slug."""
    for project in PROJECT_DATA:
        if project['slug'] == slug:
            return project
    return None

# --- 4. Routing and View Functions ---

@app.route('/')
def index():
    """
    Renders the homepage. 
    It uses index.html, which extends base.html to define the project list content.
    """
    # Passes the full list of projects to the index template.
    return render_template('index.html', projects=PROJECT_DATA)

@app.route('/project/<slug>')
def project_detail(slug):
    """
    Renders the detailed view for a specific project based on the slug parameter.
    """
    project = get_project_by_slug(slug)
    
    if project is None:
        # If the project is not found, trigger the custom 404 handler.
        abort(404)
        
    # project_detail.html uses the 'project' data to dynamically override the 
    # {% block title %} content using project['name'].
    return render_template('project_detail.html', project=project)

# --- 5. Error Handling (Demonstrating inheritance consistency) ---

@app.errorhandler(404)
def page_not_found(error):
    """
    Custom 404 error handler. 
    Crucially, '404.html' also extends 'base.html' to ensure the error page 
    maintains the site's consistent header, navigation, and footer.
    """
    # The status code (404) must be returned explicitly.
    return render_template('404.html'), 404

# --- 6. Execution ---
if __name__ == '__main__':
    # For instructional purposes, we assume the template files are correctly placed.
    # To run this script: app.run(debug=True)
    pass
