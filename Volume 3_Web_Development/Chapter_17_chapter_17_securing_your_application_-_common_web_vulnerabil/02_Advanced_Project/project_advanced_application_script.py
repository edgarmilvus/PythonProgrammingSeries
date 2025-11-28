
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

import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# --- 1. Database Setup and Initialization ---

DATABASE = 'secure_notes.db'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    # This function ensures the connection is ready for use
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def init_db():
    """Initializes the database schema if it doesn't exist."""
    conn = get_db_connection()
    # Create a simple table to store notes
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

# --- 2. CSRF and Form Definition (Using Flask-WTF) ---

class NoteForm(FlaskForm):
    """Defines the form structure for adding a new note."""
    # DataRequired validator ensures the field is not empty
    # Flask-WTF automatically includes a hidden CSRF token field
    note_content = StringField('Note Content', validators=[DataRequired()])
    submit = SubmitField('Post Secure Note')

# --- 3. Flask Application Setup ---

app = Flask(__name__)
# CRITICAL: Secret key is required for session management and CSRF protection
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_very_secret_and_complex_key_12345')
init_db() # Initialize the database on startup

# --- 4. Database Operations with SQL Injection Prevention ---

def add_note(content):
    """Inserts a new note using parameterized queries (SQLi defense)."""
    conn = get_db_connection()
    try:
        # DEFENSE: Parameterized Query (using '?')
        # The content is passed separately as a tuple, preventing it from being interpreted as SQL
        conn.execute("INSERT INTO notes (content) VALUES (?)", (content,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error during insertion: {e}")
    finally:
        conn.close()

def get_all_notes():
    """Fetches all notes from the database."""
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes ORDER BY id DESC').fetchall()
    conn.close()
    return notes

# --- 5. Application Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handles displaying the notes and processing the form."""
    form = NoteForm()
    
    # DEFENSE: CSRF Validation
    # validate_on_submit() checks if the request is POST and if the CSRF token is valid
    if form.validate_on_submit():
        note_content = form.note_content.data
        
        # SQLi Prevention happens inside add_note()
        add_note(note_content)
        
        # Use POST/Redirect/GET pattern to prevent duplicate submissions
        return redirect(url_for('index'))

    notes = get_all_notes()
    
    # Rendering the template (where XSS defense occurs via Jinja2 auto-escaping)
    return render_template('index.html', form=form, notes=notes)

if __name__ == '__main__':
    # NOTE: In a real application, never use debug=True in production.
    app.run(debug=True)

# --- 6. Required Template Content (index.html, stored separately in practice) ---
# For demonstration purposes, assume index.html contains:
"""
<!doctype html>
<title>Secure Notes</title>
<h1>Post a New Note</h1>
<form method="POST">
    {{ form.hidden_tag() }} <!-- Renders the hidden CSRF token -->
    {{ form.note_content.label }}: {{ form.note_content() }}
    {% for error in form.note_content.errors %}
        <span style="color: red;">[{{ error }}]</span>
    {% endfor %}
    {{ form.submit() }}
</form>
<hr>
<h2>Recent Notes</h2>
{% for note in notes %}
    <p>ID: {{ note.id }}</p>
    <!-- DEFENSE: XSS Prevention -->
    <!-- Jinja2 automatically escapes content (e.g., converts <script> to &lt;script&gt;) -->
    <p>Content: {{ note.content }}</p> 
    <hr>
{% endfor %}
"""
