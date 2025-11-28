
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

import os
from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError

# --- 1. WTForms Definition ---

# Define a custom validator to prevent overly long names
def max_length_check(form, field):
    """Custom validator to ensure a field is not excessively long."""
    if len(field.data) > 50:
        raise ValidationError('Input exceeds the maximum allowed length of 50 characters.')

class EventRegistrationForm(FlaskForm):
    """
    Defines the structure and validation rules for the event registration form.
    FlaskForm automatically handles CSRF token generation and validation.
    """
    
    # Name field: Must be present (DataRequired) and pass the custom length check.
    name = StringField(
        'Full Name',
        validators=[DataRequired(message="Name is required."), max_length_check]
    )

    # Email field: Must be present and conform to standard email format.
    email = EmailField(
        'Email Address',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Invalid email format."),
            Length(max=100, message="Email cannot exceed 100 characters.")
        ]
    )

    # Event selection: Limited choices to prevent arbitrary input.
    event_choice = SelectField(
        'Select Event',
        choices=[
            ('ai_summit', 'AI & Machine Learning Summit'),
            ('web_dev_conf', 'Modern Web Development Conference'),
            ('data_sci_boot', 'Data Science Bootcamp')
        ],
        validators=[DataRequired(message="Please select an event.")]
    )
    
    # Optional field with basic length validation
    comments = TextAreaField(
        'Comments (Optional)',
        validators=[Length(max=300, message="Comments must be under 300 characters.")],
        render_kw={"rows": 3} # HTML rendering hint
    )

    # Submit button
    submit = SubmitField('Register Now')


# --- 2. Flask Application Setup ---

# Initialize Flask application
app = Flask(__name__)

# CRITICAL: Secret key is required for session management, flash messages, 
# and Flask-WTF's CSRF protection.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-secret-key-12345')

# In-memory storage for demonstration (simulating a database)
REGISTERED_ATTENDEES = []

# --- 3. Route Handlers ---

@app.route('/', methods=['GET', 'POST'])
def register():
    """
    Handles the display and processing of the registration form.
    Implements the Post/Redirect/Get (PRG) pattern upon successful submission.
    """
    form = EventRegistrationForm() # Instantiate the form

    # Check if the request is POST and if all validators passed (including CSRF check)
    if form.validate_on_submit():
        
        # --- Data Processing and Sanitization ---
        # Data is already moderately sanitized by WTForms (e.g., stripping whitespace)
        # and validated against types/lengths. We retrieve the clean data.
        
        name_clean = form.name.data.strip()
        email_clean = form.email.data.lower()
        event_clean = form.event_choice.data
        comments_clean = form.comments.data.strip()

        # Simulate storing the data securely
        registration_record = {
            'name': name_clean,
            'email': email_clean,
            'event': event_clean,
            'comments': comments_clean
        }
        REGISTERED_ATTENDEES.append(registration_record)
        
        # Use Flask's flash message system to notify the user of success
        flash(f"Successfully registered {name_clean} for the {event_clean.replace('_', ' ').title()}!", 'success')
        
        # CRITICAL: Implement PRG pattern to prevent form resubmission on refresh
        return redirect(url_for('register')) 

    # If GET request or validation failed, render the template
    # The form object passed to the template will contain any validation errors
    # (e.g., form.name.errors) which the template can display.
    return render_template('register.html', form=form, attendees=REGISTERED_ATTENDEES)


# --- 4. Template Placeholder (Assumed HTML for Context) ---
# NOTE: In a real application, 'register.html' would exist and contain:
"""
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        <ul class=flashes>
        {% for category, message in messages %}
            <li class="{{ category }}">{{ message }}</li>
        {% endfor %}
        </ul>
    {% endif %}
{% endwith %}

<form method="POST">
    {{ form.hidden_tag() }} <!-- Renders the CSRF token -->
    {{ form.name.label }} {{ form.name() }}
    {% for error in form.name.errors %} <span>{{ error }}</span> {% endfor %}
    <!-- ... other fields ... -->
    {{ form.submit() }}
</form>
"""

# Example route to view stored data (for debugging/verification)
@app.route('/attendees')
def list_attendees():
    return f"<h2>Registered Users ({len(REGISTERED_ATTENDEES)})</h2><pre>{REGISTERED_ATTENDEES}</pre>"

if __name__ == '__main__':
    # Setting debug=True for development, but requires a strong SECRET_KEY in production
    app.run(debug=True)
