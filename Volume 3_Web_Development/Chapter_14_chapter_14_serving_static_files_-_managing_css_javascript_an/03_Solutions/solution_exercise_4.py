
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

import os
from flask import Flask, render_template, current_app, url_for

# --- 1. Configuration Setup ---
class Config:
    # Requirement 1: Define the ASSET_VERSION
    ASSET_VERSION = '1.0.0'
    STATIC_FOLDER = os.path.join(os.getcwd(), 'static')

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object(Config)

# (Setup code for creating dummy files omitted for brevity, assume 'static/main.css' exists)

# --- 2. Context Processor (Requirement 2) ---
@app.context_processor
def inject_asset_version():
    """
    Injects the ASSET_VERSION variable into every template render context.
    """
    return dict(ASSET_VERSION=current_app.config['ASSET_VERSION'])

# --- 3. Route Definition ---
@app.route('/static_version')
def static_version_index():
    # Renders the template that uses the static version
    return render_template('static_index.html')

# --- JINJA TEMPLATE (templates/static_index.html) ---

# Requirement 3 & 4: Template Modification
STATIC_VERSION_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Static Versioned Assets</title>
    
    <!-- MODIFIED LINK (After Requirement 3): -->
    <link rel="stylesheet" 
          href="{{ url_for('static', filename='main.css', v=ASSET_VERSION) }}">
</head>
<body>
    <h1>Testing Static Cache Busting</h1>
    <p>Check the source code: The URL should be 
       /static/main.css?v=1.0.0</p>
</body>
</html>
"""

# Example verification output (HTML source):
# <link rel="stylesheet" href="/static/main.css?v=1.0.0">
