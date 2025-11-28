
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

# Source File: solution_exercise_8.py
# Description: Solution for Exercise 8
# ==========================================

from flask import Flask, render_template, url_for
from reports.routes import reports_bp # Assuming reports/routes.py is available

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'

    # Main application route
    @app.route('/')
    def index():
        # Renders templates/main_index.html
        return render_template('main_index.html')

    @app.route('/test_main_static')
    def test_main_static():
        # Demonstrates URL generation for the main application's static files
        static_url = url_for('static', filename='style.css')
        return f"Main Static URL: {static_url}", 200

    # Register the reports blueprint
    app.register_blueprint(reports_bp)
    return app

# --- Verification Logic ---
app = create_app()
with app.test_client() as client:
    print("\n--- Static File Isolation Verification ---")

    # 1. Main App Static Check (Uses the application's default static folder)
    main_static_response = client.get('/test_main_static')
    print(f"Main App Static URL: {main_static_response.data.decode()}")
    # Expected URL: /static/style.css

    # 2. Reports Blueprint Static Check (Uses the blueprint's isolated static folder)
    reports_static_response = client.get('/reports/test_static')
    print(f"Reports Blueprint Static URL: {reports_static_response.data.decode()}")
    # Expected URL: /reports/static/style.css
