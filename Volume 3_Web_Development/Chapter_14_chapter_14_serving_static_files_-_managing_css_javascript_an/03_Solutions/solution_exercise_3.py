
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

# Source File: solution_exercise_3.py
# Description: Solution for Exercise 3
# ==========================================

from flask import Flask, render_template, Blueprint
import os

# --- 1. Blueprint Setup ---
# Configure the Blueprint to use its own static folder
admin_bp = Blueprint('admin_bp', __name__, 
                     template_folder='templates',
                     static_folder=os.path.join(os.path.dirname(__file__), 'admin', 'static'),
                     static_url_path='/admin/assets') # Optional: Custom URL path for Blueprint assets

app = Flask(__name__)

# --- Blueprint Routes ---
@admin_bp.route('/dashboard')
def dashboard():
    # Renders admin_dashboard.html
    return render_template('admin_dashboard.html')

# --- Main Application Routes ---
@app.route('/')
def index():
    # Renders index.html
    return render_template('index.html')

# Register the Blueprint
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == '__main__':
    # Example URL generation analysis:
    # Main app static URL: /static/banner.css
    # Blueprint static URL: /admin/assets/banner.css
    
    # Analysis of Resolution:
    # 1. Main Route (`/`): Uses url_for('static', ...). Flask resolves this to the 
    #    main application's static folder: /static/banner.css (RED background).
    
    # 2. Admin Route (`/admin/dashboard`): Uses url_for('admin_bp.static', ...). 
    #    By explicitly using the Blueprint endpoint, Flask resolves this to the 
    #    Blueprint's configured static folder: /admin/assets/banner.css (BLUE background).
    
    # If the admin route had mistakenly used url_for('static', ...), it would have 
    # loaded the main application's RED CSS, demonstrating the importance of
    # specifying the Blueprint endpoint for isolated assets.
    
    # app.run(debug=True)
    pass
