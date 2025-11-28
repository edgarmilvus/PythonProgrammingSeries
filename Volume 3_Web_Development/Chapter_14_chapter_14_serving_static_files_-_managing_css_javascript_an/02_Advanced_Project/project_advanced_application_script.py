
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
import time
from pathlib import Path
from flask import Flask, render_template_string, url_for

# --- 1. Configuration and Setup ---

# Define the root directory for the app
APP_ROOT = Path(__file__).parent
STATIC_DIR = APP_ROOT / 'static'
TEMPLATES_DIR = APP_ROOT / 'templates'

# Ensure directories exist for Flask to function correctly
STATIC_DIR.mkdir(exist_ok=True)
(STATIC_DIR / 'css').mkdir(exist_ok=True)
(STATIC_DIR / 'js').mkdir(exist_ok=True)
(STATIC_DIR / 'images').mkdir(exist_ok=True)

# --- 2. Static File Simulation (Creating necessary assets) ---

def create_dummy_assets():
    """Generates dummy CSS, JS, and image files for demonstration."""
    
    # Standard site CSS (will be cache busted)
    css_content = f"""
body {{ font-family: 'Arial', sans-serif; background-color: #f4f4f9; }}
.header {{ padding: 20px; background-color: #333; color: white; text-align: center; }}
.version-tag {{ font-size: 0.8em; color: #ccc; }}
/* Last Modified: {time.time()} */
"""
    (STATIC_DIR / 'css' / 'main.css').write_text(css_content.strip())

    # Project-specific CSS (used only on the project page)
    (STATIC_DIR / 'css' / 'project_a.css').write_text(".project-box { border: 2px solid #007bff; padding: 15px; }")

    # JavaScript file (for interactivity)
    js_content = "console.log('Portfolio scripts loaded successfully.');"
    (STATIC_DIR / 'js' / 'main.js').write_text(js_content)

    # Image placeholder (simulated)
    (STATIC_DIR / 'images' / 'profile.png').touch()
    
    print("Dummy assets created.")

# Initialize dummy assets
create_dummy_assets()

# --- 3. Flask Application Initialization ---

app = Flask(__name__,
            static_folder=STATIC_DIR,
            template_folder=TEMPLATES_DIR)

# --- 4. Cache Busting Utility Function ---

def cache_busted_url_for(endpoint, **values):
    """
    Custom helper that wraps url_for and adds a cache busting parameter 
    based on the file's modification time (mtime).
    """
    if endpoint == 'static':
        filename = values.get('filename')
        if filename:
            # Construct the absolute path to the static file
            static_file_path = Path(app.static_folder) / filename
            
            # Check if the file exists
            if static_file_path.exists():
                # Get the modification timestamp (mtime)
                mtime = int(static_file_path.stat().st_mtime)
                
                # Add the timestamp as a query parameter 'v' (version)
                values['v'] = mtime
                
    # Call the original Flask url_for function
    return url_for(endpoint, **values)

# Register the custom function so it can be used directly in templates
app.jinja_env.globals['static_url'] = cache_busted_url_for

# --- 5. Template Definitions (Stored as strings for script cohesion) ---

# Base template defining the structure and linking main assets
BASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Portfolio Showcase{% endblock %}</title>
    <!-- Standard external CSS link using the cache busting helper -->
    <link rel="stylesheet" href="{{ static_url('static', filename='css/main.css') }}">
    {% block extra_head %}{% endblock %}
</head>
<body>
    <div class="header">
        <h1>My Developer Portfolio</h1>
        <p class="version-tag">Assets served with cache busting.</p>
    </div>
    <div class="content">
        {% block content %}{% endblock %}
    </div>
    <!-- Standard external JavaScript link -->
    <script src="{{ static_url('static', filename='js/main.js') }}"></script>
</body>
</html>
"""

# Index route template
INDEX_HTML = """
{% extends "base.html" %}
{% block content %}
    <h2>Welcome</h2>
    <p>View my featured projects:</p>
    <ul>
        <li><a href="{{ url_for('project_detail', name='Project A') }}">Project A: Flask Dashboard</a></li>
        <li><a href="{{ url_for('project_detail', name='Project B') }}">Project B: AI Embeddings Tool</a></li>
    </ul>
    <!-- Example of an image link -->
    <img src="{{ static_url('static', filename='images/profile.png') }}" alt="Profile Image" width="50">
{% endblock %}
"""

# Project detail route template
PROJECT_HTML = """
{% extends "base.html" %}
{% block title %}Project: {{ project_name }}{% endblock %}

{% block extra_head %}
    <!-- Project specific stylesheet link (only loaded here) -->
    {% if project_name == 'Project A' %}
    <link rel="stylesheet" href="{{ static_url('static', filename='css/project_a.css') }}">
    {% endif %}
{% endblock %}

{% block content %}
    <h3>Details for {{ project_name }}</h3>
    <p class="project-box">This project demonstrates advanced static file management and dynamic template inheritance.</p>
    <p><a href="{{ url_for('index') }}">Back to Index</a></p>
{% endblock %}
"""

# --- 6. Route Definitions ---

@app.route('/')
def index():
    # Note: Flask automatically finds templates in the 'templates' folder.
    # We use render_template_string here for script portability.
    return render_template_string(BASE_HTML + INDEX_HTML)

@app.route('/project/<name>')
def project_detail(name):
    return render_template_string(BASE_HTML + PROJECT_HTML, project_name=name)

# --- 7. Execution ---

if __name__ == '__main__':
    print(f"Application running. Static folder: {STATIC_DIR}")
    
    # Example usage demonstration (simulating a request and checking the URL)
    with app.test_request_context('/'):
        # This will print the generated URL with the cache-busting timestamp
        main_css_url = cache_busted_url_for('static', filename='css/main.css')
        print(f"Generated CSS URL: {main_css_url}")
        
    # To demonstrate cache busting, let's update the file and check the URL again
    time.sleep(1) # Ensure mtime changes
    (STATIC_DIR / 'css' / 'main.css').write_text("Updated content.")
    
    with app.test_request_context('/'):
        updated_css_url = cache_busted_url_for('static', filename='css/main.css')
        print(f"Updated CSS URL: {updated_css_url}")
        
    print("\nIf the timestamps (v=...) differ, cache busting is successful.")
    
    # Clean up dummy files (optional, but good practice)
    import shutil
    shutil.rmtree(STATIC_DIR, ignore_errors=True)
    
    # app.run(debug=True) # Uncomment to run the server
