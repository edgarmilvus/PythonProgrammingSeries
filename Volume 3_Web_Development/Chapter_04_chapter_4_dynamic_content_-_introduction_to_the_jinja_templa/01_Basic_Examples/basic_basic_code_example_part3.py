
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

# Source File: basic_basic_code_example_part3.py
# Description: Basic Code Example
# ==========================================

template_string = """
<!DOCTYPE html>
<html>
<!-- ... standard HTML structure ... -->

    <!-- Jinja variable rendering syntax: {{ ... }} -->
    <h1>Welcome, {{ user_name }}!</h1>
    
    <!-- Jinja filter usage: | filter_name(args) -->
    <p>Current Price: <strong>${{ price | round(2) }}</strong>.</p>
    
    <!-- Jinja control structure syntax: {% ... %} -->
    {% if is_premium %}
        <p style="color: green;">As a premium member, you qualify for an immediate 10% discount!</p>
    {% else %}
        <p style="color: orange;">Sign up for our premium tier today to unlock exclusive benefits!</p>
    {% endif %}
<!-- ... closing tags ... -->
"""
