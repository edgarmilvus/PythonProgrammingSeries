
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

from flask import Flask, request, abort, jsonify

# 1. Application Setup and Initialization
app = Flask(__name__)

# 2. Simulated Database (In-memory storage for tools)
# Keys are the tool IDs, which are integers.
TOOL_DATABASE = {
    101: {"name": "WebScraper", "category": "Data Retrieval", "version": 1.2, "status": "Active"},
    102: {"name": "CodeExecutor", "category": "Execution", "version": 2.0, "status": "Active"},
    103: {"name": "ImageGenerator", "category": "Creative", "version": 1.0, "status": "Maintenance"},
    104: {"name": "DBQueryTool", "category": "Data Retrieval", "version": 1.5, "status": "Active"},
}
NEXT_ID = 105 # Tracks the next available ID for new registrations

# --- 3. Static Route: Home Page ---

@app.route('/', methods=['GET'])
def home_page():
    # Basic view function handling the root URL.
    # Specifies that only GET requests are allowed.
    return "Welcome to the AI Tool Registry Service. Use /tools to view the catalog."

# --- 4. Static Route: Listing All Resources ---

@app.route('/tools', methods=['GET'])
def list_all_tools():
    # Lists the names of all tools currently registered.
    tool_names = [data['name'] for data in TOOL_DATABASE.values()]
    # Returns a simple string Response Object.
    return f"Registered Tools ({len(tool_names)} total): {', '.join(tool_names)}"

# --- 5. Dynamic Route: Retrieving a Specific Resource by ID ---

@app.route('/tool/<int:tool_id>', methods=['GET'])
def get_tool_details(tool_id):
    # CRITICAL: Uses the <int:tool_id> converter, ensuring the URL segment is an integer.
    # The captured integer is automatically passed as the 'tool_id' argument.
    tool_data = TOOL_DATABASE.get(tool_id)

    if tool_data is None:
        # If the ID is not found, we use 'abort' to immediately generate a 404 Not Found response.
        abort(404, description=f"Tool ID {tool_id} not found in registry.")

    # Return a formatted string detailing the tool's attributes.
    return (f"Tool Details (ID: {tool_id}): "
            f"Name: {tool_data['name']}, "
            f"Category: {tool_data['category']}, "
            f"Status: {tool_data['status']}")

# --- 6. Dynamic Route: Filtering Resources by Category (String Parameter) ---

@app.route('/tools/category/<string:category_name>', methods=['GET'])
def filter_by_category(category_name):
    # Uses the <string:category_name> converter to capture a URL segment as a string.
    # The string converter is the default, but explicitly specifying it improves clarity.
    
    # Simple cleaning: replace URL slugs (e.g., data-retrieval) with readable titles.
    category_name_clean = category_name.replace('-', ' ').title() 

    filtered_tools = [
        f"{tool_id}: {data['name']}"
        for tool_id, data in TOOL_DATABASE.items()
        if data['category'].lower() == category_name_clean.lower()
    ]

    if not filtered_tools:
        # If no tools match, return a message with a 200 OK status.
        return f"No tools found in the category: {category_name_clean}", 200

    return f"Tools in '{category_name_clean}': {'; '.join(filtered_tools)}"

# --- 7. Route Handling Multiple HTTP Methods (GET and POST) ---

@app.route('/register', methods=['GET', 'POST'])
def register_new_tool():
    global NEXT_ID

    if request.method == 'POST':
        # Logic executed only when a client sends data to create a new resource.
        # We use request.args.get('name') for simple testing via URL parameters.
        new_tool_name = request.args.get('name', 'New Unnamed Tool')
        
        # Add the new tool to the simulated database.
        TOOL_DATABASE[NEXT_ID] = {
            "name": new_tool_name, 
            "category": "Uncategorized", 
            "version": 1.0, 
            "status": "Pending"
        }
        NEXT_ID += 1
        
        # Return a Response Object with a 201 Created status code.
        return f"Tool '{new_tool_name}' registered successfully with ID {NEXT_ID - 1}", 201
    
    # Logic executed if the request method is GET (e.g., a user visits the URL directly).
    return "To register a tool, send a POST request to this endpoint with the required data (e.g., tool name)."

# --- 8. Application Runner ---

if __name__ == '__main__':
    # Runs the application locally. Set debug=True for automatic reloading during development.
    app.run(debug=True)
