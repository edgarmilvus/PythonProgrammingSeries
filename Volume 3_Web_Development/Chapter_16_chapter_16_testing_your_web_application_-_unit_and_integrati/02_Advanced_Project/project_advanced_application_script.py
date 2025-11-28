
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

# 1. APPLICATION LOGIC: Task Service (Unit Test Target)
class TaskService:
    """Handles core business logic for tasks, independent of Flask."""
    def __init__(self):
        # Simple in-memory storage for demonstration
        self.tasks = []
        self.next_id = 1

    def get_all_tasks(self):
        # Returns the current list of tasks
        return self.tasks

    def add_task(self, description: str):
        """
        Validates and adds a new task. Raises ValueError on failure.
        """
        if not description or len(description.strip()) < 5:
            # Custom exception for clear testing of validation rules
            raise ValueError("Task description must be at least 5 characters long.")

        task = {
            'id': self.next_id,
            'description': description.strip(),
            'done': False
        }
        self.tasks.append(task)
        self.next_id += 1
        return task

    def clear_tasks(self):
        """Utility function to reset state between test runs."""
        self.tasks = []
        self.next_id = 1

# Initialize the service instance used by the Flask application
task_service = TaskService()

# 2. FLASK APPLICATION SETUP (Integration Test Target)
import json
import pytest
from flask import Flask, request, jsonify

def create_app():
    """Application Factory pattern for clean testing setup."""
    app = Flask(__name__)

    @app.route('/tasks', methods=['GET'])
    def list_tasks():
        # Route to fetch all tasks from the service
        return jsonify(task_service.get_all_tasks())

    @app.route('/tasks', methods=['POST'])
    def add_new_task():
        data = request.get_json(silent=True) # silent=True handles non-JSON body gracefully
        
        # Check for missing or malformed JSON
        if not data or 'description' not in data:
            return jsonify({"error": "Missing task description or invalid JSON payload"}), 400
        
        description = data['description']
        try:
            # Call the core logic service, which handles validation
            new_task = task_service.add_task(description)
            # Successful creation response, HTTP 201 Created
            return jsonify(new_task), 201
        except ValueError as e:
            # Handle validation errors raised by TaskService logic
            return jsonify({"error": str(e)}), 422 # HTTP 422 Unprocessable Entity

    return app

# 3. PYTEST FIXTURES (Setup for Integration Testing)

@pytest.fixture
def app():
    """PyTest fixture that creates and yields a clean Flask application instance."""
    app = create_app()
    # Ensure the global service state is reset before the test runs
    task_service.clear_tasks()
    yield app
    # Ensure cleanup after the test completes
    task_service.clear_tasks()

@pytest.fixture
def client(app):
    """PyTest fixture that provides the Flask test client."""
    # The test client allows simulation of HTTP requests without running a server
    return app.test_client()


# 4. UNIT TESTS (Focus on TaskService logic isolation)

def test_task_service_initial_state():
    # Verify the service starts empty and IDs are correct
    service = TaskService()
    assert service.get_all_tasks() == []
    assert service.next_id == 1

def test_task_service_add_valid_task():
    # Test successful task addition and ID management
    service = TaskService()
    task = service.add_task("Write PyTest chapter draft")
    assert len(service.get_all_tasks()) == 1
    assert task['id'] == 1

def test_task_service_validation_failure():
    # Test failure when description is too short, relying on Python's exception handling
    service = TaskService()
    with pytest.raises(ValueError) as excinfo:
        service.add_task("four")
    # Verify the error message matches the business rule
    assert "at least 5 characters" in str(excinfo.value)
    assert len(service.get_all_tasks()) == 0


# 5. INTEGRATION TESTS (Focus on HTTP behavior and routes)

def test_get_tasks_empty(client):
    # Integration test: Check GET /tasks returns an empty list (200 OK)
    response = client.get('/tasks')
    assert response.status_code == 200
    assert response.get_json() == []

def test_post_task_success(client):
    # Integration test: Successful POST request (201 Created)
    task_data = {'description': 'Review testing documentation'}
    response = client.post(
        '/tasks',
        data=json.dumps(task_data),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['description'] == task_data['description']
    assert data['id'] == 1

    # Verify state change: Check if the task now appears in the GET endpoint
    get_response = client.get('/tasks')
    assert len(get_response.get_json()) == 1

def test_post_task_validation_error(client):
    # Integration test: POST request triggering TaskService validation (422 Unprocessable Entity)
    response = client.post(
        '/tasks',
        data=json.dumps({'description': 'fail'}),
        content_type='application/json'
    )
    assert response.status_code == 422
    data = response.get_json()
    assert "at least 5 characters" in data['error']

def test_post_task_missing_payload(client):
    # Integration test: POST request with missing description field (400 Bad Request)
    response = client.post(
        '/tasks',
        data=json.dumps({'title': 'irrelevant'}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing task description" in data['error']
