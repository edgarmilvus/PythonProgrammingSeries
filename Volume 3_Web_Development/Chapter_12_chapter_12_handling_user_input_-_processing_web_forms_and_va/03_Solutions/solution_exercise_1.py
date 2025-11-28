
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

import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

# --- Setup ---
app = Flask(__name__)
# CRITICAL: Flask-WTF requires a secret key for security (CSRF protection)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_very_secret_key_for_dev')


# --- WTForms Definitions (For Exercises 3 and 4) ---

class RegistrationForm(FlaskForm):
    """Form for Exercise 3: User Registration."""
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=4, max=20, message="Username must be between 4 and 20 characters.")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address format.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Confirmation password is required."),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')

class RAGConfigForm(FlaskForm):
    """Form for Exercise 4: RAG Configuration Update."""
    model_name = StringField('LLM Model Name', validators=[DataRequired()])
    vector_store_path = StringField('Vector Store Path', validators=[DataRequired()])
    
    # E4.1, E4.2, E4.3: Add temperature field with NumberRange validation
    temperature = FloatField('LLM Temperature (0.0 to 1.0)', validators=[
        DataRequired(message="Temperature is required."),
        # Ensures the float value is strictly within the acceptable range
        NumberRange(min=0.0, max=1.0, message="Temperature must be between 0.0 and 1.0 inclusive.")
    ])
    submit = SubmitField('Update Configuration')


# --- Exercise 1 & 5: Basic Feedback Collector ---

@app.route('/feedback', methods=['GET', 'POST'])
def handle_feedback():
    """Handles basic feedback collection and demonstrates Jinja's default escaping (E5)."""
    if request.method == 'POST':
        feedback_type = request.form.get('feedback_type', 'N/A')
        message = request.form.get('message', 'No message provided')
        
        # E5: Security Focus - Sanitizing User Input for Display
        # Jinja's autoescaping is enabled by default in Flask. 
        # When 'message' is rendered in the template using {{ message }}, 
        # any HTML (like <script> tags) will be converted to harmless entities 
        # (&lt;script&gt;), preventing Cross-Site Scripting (XSS) attacks.
        # This reliance on default escaping is a mandatory security practice.
        
        return render_template('feedback_received.html', 
                               feedback_type=feedback_type, 
                               message=message) 
    
    return render_template('feedback_form.html')


# --- Exercise 2: Server-Side Validation (Event Registration) ---

@app.route('/register_event', methods=['GET', 'POST'])
def register_event():
    """Handles event registration with manual, robust server-side validation."""
    errors = []
    data = {} # Used to repopulate the form fields if validation fails
    
    if request.method == 'POST':
        name = request.form.get('attendee_name', '').strip()
        date_str = request.form.get('event_date', '').strip()
        tickets_str = request.form.get('num_tickets', '').strip()
        
        # Store submitted data to repopulate form
        data = request.form 

        # E2.1: Basic Validation (Name)
        if not name:
            errors.append("Attendee Name is required.")

        # E2.2: Ticket Validation (Integer conversion and positive check)
        num_tickets = None
        if not tickets_str:
            errors.append("Number of tickets is required.")
        else:
            try:
                num_tickets = int(tickets_str)
                if num_tickets <= 0:
                    errors.append("Number of tickets must be greater than zero.")
            except ValueError:
                errors.append("Number of tickets must be a valid integer.")

        # E2.3: Date Validation using datetime.strptime()
        event_date = None
        if not date_str:
            errors.append("Event Date is required.")
        else:
            try:
                # CRITICAL: Parsing the string into a datetime object using the required format
                event_date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                errors.append("Event Date is invalid. Required format: YYYY-MM-DD.")
        
        if errors:
            # If errors exist, re-render the form with error messages and submitted data
            return render_template('register_event.html', errors=errors, data=data), 400
        
        # Success path
        return render_template('registration_success.html', 
                               name=name, 
                               date=event_date.strftime("%B %d, %Y"), 
                               tickets=num_tickets)

    # Initial GET request
    return render_template('register_event.html', errors=[], data={})


# --- Exercise 3: WTForms Registration ---

@app.route('/wtforms_register', methods=['GET', 'POST'])
def wtforms_register():
    """Handles user registration using WTForms for validation."""
    form = RegistrationForm()
    
    # validate_on_submit() checks for POST method AND runs all validators
    if form.validate_on_submit():
        # Data is valid and ready for processing (e.g., saving to database)
        print(f"User Registered: {form.username.data}, Email: {form.email.data}")
        return redirect(url_for('registration_complete'))
    
    # If GET or validation failed, render the form (WTForms handles error display automatically)
    return render_template('wtforms_register.html', form=form)

@app.route('/registration_complete')
def registration_complete():
    return "<h1>Registration Complete!</h1><p>WTForms handled the validation successfully.</p>"


# --- Exercise 4: Interactive Challenge Route (RAG Configuration) ---

@app.route('/config_update', methods=['GET', 'POST'])
def config_update():
    """Handles RAG configuration update, demonstrating FloatField and NumberRange validator."""
    form = RAGConfigForm()
    
    if form.validate_on_submit():
        # The NumberRange validator guarantees that form.temperature.data is 0.0 <= T <= 1.0
        temp = form.temperature.data
        
        # Simulate configuration update
        print(f"RAG Config Updated. Temperature set to: {temp}")
        return f"<h1>Config Success</h1><p>LLM Temperature: {temp}</p>"
    
    # If GET or validation failed (e.g., temperature > 1.0), render the form
    return render_template('rag_config.html', form=form)


if __name__ == '__main__':
    # Running locally requires templates folder setup
    # app.run(debug=True)
    pass
