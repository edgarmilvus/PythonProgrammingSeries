
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
from flask import Flask, render_template, request, abort

# --- 1. Static Data Source (Simulating a database fetch) ---
PROJECT_DATA = [
    {"id": 101, "name": "Q3 API Migration", "status": "Completed", "priority": "High", "progress": 100, "assigned": "Alice Johnson"},
    {"id": 102, "name": "Frontend Redesign", "status": "In Progress", "priority": "Medium", "progress": 45, "assigned": "Bob Smith"},
    {"id": 103, "name": "Database Optimization", "status": "Blocked", "priority": "High", "progress": 10, "assigned": "Charlie Brown"},
    {"id": 104, "name": "Documentation Update", "status": "In Progress", "priority": "Low", "progress": 80, "assigned": "Diana Prince"},
    {"id": 105, "name": "Server Maintenance", "status": "Pending", "priority": "Medium", "progress": 0, "assigned": "Eve Adams"},
    {"id": 106, "name": "Security Audit", "status": "Completed", "priority": "High", "progress": 100, "assigned": "Alice Johnson"},
]

# --- 2. Application Setup ---
# Initialize Flask app instance
app = Flask(__name__)

# Basic configuration (using environment variable for security key if available)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_dev_key')
app.config['ENV'] = 'development'
app.config['DEBUG'] = True


# --- 3. Helper Function for Data Filtering ---
def get_filtered_projects(status_filter=None):
    """Filters the global project data based on an optional status string."""
    if status_filter and status_filter.lower() != 'all':
        # List comprehension to filter projects matching the required status
        return [
            project for project in PROJECT_DATA 
            if project['status'].lower() == status_filter.lower()
        ]
    # Return all projects if no filter is provided or if 'all' is requested
    return PROJECT_DATA


# --- 4. Route: Main Dashboard (Handling loops and conditionals) ---
@app.route('/')
def dashboard():
    """
    Renders the main dashboard, allowing filtering via URL query parameters.
    Example: /?status=In%20Progress
    """
    # Check for a 'status' query parameter in the URL (e.g., ?status=Completed)
    status_filter = request.args.get('status')
    
    # Use the helper function to get the relevant dataset
    projects = get_filtered_projects(status_filter)
    
    # Prepare metadata for the template
    current_filter = status_filter if status_filter else 'All'
    
    # Render the template, passing the dynamic data
    # Jinja will use loops (for) and conditionals (if) to build the HTML table/cards
    return render_template(
        'dashboard.html', 
        projects=projects,
        filter_applied=current_filter,
        total_projects=len(PROJECT_DATA)
    )


# --- 5. Route: Project Detail View (Handling simple variable rendering) ---
@app.route('/project/<int:project_id>')
def project_detail(project_id):
    """
    Renders a detailed view for a single project based on the ID provided in the URL.
    """
    # Search the list for the matching project ID
    project = next((p for p in PROJECT_DATA if p['id'] == project_id), None)
    
    # If the project is not found, raise a 404 error
    if project is None:
        # Flask's abort function automatically triggers the appropriate error page
        abort(404)
        
    # Render the detail template, passing the single project dictionary
    return render_template(
        'project_detail.html', 
        project=project,
        title=f"Details for {project['name']}"
    )


# --- 6. Error Handler (Example of templating error pages) ---
@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 error page handler."""
    # We can also render a template for error pages, ensuring a consistent look
    return render_template('404.html'), 404


# --- 7. Application Entry Point ---
if __name__ == '__main__':
    # Running the application
    app.run(host='0.0.0.0', port=5000)
