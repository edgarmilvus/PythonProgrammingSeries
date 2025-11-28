
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

# app.py
from flask import Flask, render_template, abort

app = Flask(__name__)

# Route 1: Home page
@app.route('/')
def index():
    return render_template('index.html', active_page='home')

# Route 2: About page
@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

# Route 3: Dashboard page (Exercise 4)
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

# Route 4: Test 404 trigger (Exercise 3)
@app.route('/test_404')
def test_404():
    # Intentionally raises a 404 error
    abort(404) 

# Flask error handler for 404 (Exercise 3)
@app.errorhandler(404)
def page_not_found(e):
    # Render the custom 404 template and set the HTTP status code
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
