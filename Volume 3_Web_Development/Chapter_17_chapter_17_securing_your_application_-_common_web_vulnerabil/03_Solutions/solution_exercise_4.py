
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

from markupsafe import Markup

@app.route('/manual_escape_demo')
def manual_escape_demo():
    user_input = request.args.get('data', '<b>Test</b>')
    
    # Manual Escaping: Converts characters like <, >, &, and " into HTML entities.
    safe_output = Markup.escape(user_input)
    
    print(f"Original Input: {user_input}")
    print(f"Escaped Output: {safe_output}")
    
    # In a template where auto-escaping is off, we would render safe_output.
    return f"<h1>Manually Escaped:</h1><p>{safe_output}</p>"

# Explanation:
# Manual escaping is generally discouraged because it requires the developer to remember 
# to apply the escape function everywhere untrusted data is rendered. 
# Relying on the framework's default auto-escaping (like Jinja's) ensures that 
# escaping is applied globally and consistently by default, significantly reducing 
# the chance of human error leading to XSS vulnerabilities.
