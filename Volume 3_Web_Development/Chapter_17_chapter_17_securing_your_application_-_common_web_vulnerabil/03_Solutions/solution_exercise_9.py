
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

# Source File: solution_exercise_9.py
# Description: Solution for Exercise 9
# ==========================================

import re
from flask import request, render_template, abort

# Define a simple template content for greeting.html (conceptual)
GREETING_TEMPLATE = """
<!doctype html>
<title>Greeting</title>
<h1>Hello, {{ name }}!</h1>
<p>Your input was rendered safely.</p>
"""

@app.route('/greeting')
def secure_greeting():
    name = request.args.get('name', 'Guest')
    
    # Input Validation (Requirement 4): Allow only alphanumeric characters and spaces
    if not re.match(r'^[a-zA-Z0-9\s]+$', name):
        # Fail fast: Reject input that contains malicious characters
        abort(400, description="Invalid characters detected in name parameter.")

    # Secure Rendering (Requirement 2): Jinja's auto-escaping is the primary defense here.
    return render_template('greeting.html', name=name)

# Mock template rendering function (since we aren't using file system templates)
def render_template(template_name, **context):
    if template_name == 'greeting.html':
        # Simulate Jinja rendering with auto-escaping
        name = context['name']
        
        # Test payload: name=<script>console.log('XSS')</script>
        # Auto-escaping converts the input to:
        # &lt;script&gt;console.log(&#39;XSS&#39;)&lt;/script&gt;
        
        # We simulate the safe rendering result:
        safe_name = name.replace('<', '&lt;').replace('>', '&gt;')
        return GREETING_TEMPLATE.replace('{{ name }}', safe_name)
    return "Template not found."
