
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

# Source File: basic_basic_code_example.py
# Description: Basic Code Example
# ==========================================

from jinja2 import Template

# 1. Define the dynamic data (the context dictionary)
# This dictionary represents the data retrieved from a database or API
user_data = {
    "user_name": "Alexandria",
    "product": "Python Expert Series",
    "price": 99.99,
    "is_premium": True
}

# 2. Define the Jinja template string
# This string contains standard HTML mixed with Jinja syntax
template_string = """
<!DOCTYPE html>
<html>
<head><title>Welcome</title></head>
<body>

    <!-- Jinja variable rendering syntax: {{ ... }} -->
    <h1>Welcome, {{ user_name }}!</h1>
    
    <p>We are excited you are interested in the <strong>{{ product }}</strong>.</p>
    
    <!-- Jinja filter usage: | filter_name(args) -->
    <p>Current Price: <strong>${{ price | round(2) }}</strong>.</p>
    
    <!-- Jinja control structure syntax: {% ... %} -->
    {% if is_premium %}
        <p style="color: green;">As a premium member, you qualify for an immediate 10% discount!</p>
    {% else %}
        <p style="color: orange;">Sign up for our premium tier today to unlock exclusive benefits!</p>
    {% endif %}
    
    <p>Thank you for joining us.</p>
</body>
</html>
"""

# 3. Create the Template object
# The Template class compiles the template string for efficient rendering
template = Template(template_string)

# 4. Render the template using the defined context data
# The render method injects the key-value pairs from user_data into the template
rendered_output = template.render(**user_data)

# 5. Display the result
print("--- Generated HTML Output ---")
print(rendered_output)
print("-----------------------------")
