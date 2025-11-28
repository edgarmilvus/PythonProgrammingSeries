
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
import logging
from flask import Flask, Blueprint, jsonify, request, url_for, current_app

# --- 1. Configuration Classes (Simulating config.py) ---

class Config:
    """Base configuration class with common settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A_very_hard_to_guess_default_key_for_base'
    LOG_LEVEL = logging.INFO
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROJECT_NAME = "Modular Dashboard"

class DevelopmentConfig(Config):
    """Configuration specific to the development environment."""
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    # In a real app, this might point to a local SQLite DB
    DATABASE_URI = 'sqlite:///dev_db.sqlite'

class ProductionConfig(Config):
    """Configuration specific to the production environment."""
    DEBUG = False
    LOG_LEVEL = logging.WARNING
    # In a real app, this would be a secure, external database
    DATABASE_URI = 'postgresql://produser:secure@prodserver/prod_db'
    # Override base secret key with a mandatory environment variable
    SECRET_KEY = os.environ.get('PRODUCTION_SECRET_KEY')

# Map configuration names to classes
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# --- 2. Extension and Utility Initialization (Simulating utils.py) ---

def configure_logging(app):
    """Sets up application-wide logging based on the loaded configuration."""
    log_level = app.config['LOG_LEVEL']
    
    # Basic configuration for demonstration
    logging.basicConfig(level=log_level, format='[%(asctime)s] %(levelname)s: %(message)s')
    
    if app.config.get('DEBUG'):
        app.logger.info("Application running in DEBUG mode.")
    else:
        app.logger.warning("Application running in production mode.")

def init_extensions(app):
    """Placeholder function to initialize external extensions (e.g., SQLAlchemy, Mail)."""
    # In a real application, this is where db.init_app(app) or mail.init_app(app) would go.
    app.logger.debug("Initializing application extensions...")
    configure_logging(app)

# --- 3. Blueprint Definitions (Simulating blueprints/core.py) ---

# Define the 'core' Blueprint for general utilities and the homepage
core_bp = Blueprint('core', __name__, url_prefix='/')

@core_bp.route('/')
def index():
    """The main entry point, accessible via the core blueprint."""
    # Use url_for to generate a link to an endpoint in the 'reporting' blueprint
    report_url = url_for('reporting.summary')
    return jsonify({
        "status": "ok",
        "message": f"Welcome to the {current_app.config['PROJECT_NAME']} Dashboard!",
        "report_link": report_url
    })

@core_bp.route('/info')
def server_info():
    """Displays configuration details for debugging purposes."""
    return jsonify({
        "environment": "Development" if current_app.config['DEBUG'] else "Production",
        "log_level": str(current_app.config['LOG_LEVEL']),
        "app_name": current_app.config['PROJECT_NAME']
    })

# --- 4. Blueprint Definitions (Simulating blueprints/reporting.py) ---

# Define the 'reporting' Blueprint for data-intensive routes
# Note: This blueprint will be registered with a global prefix later.
reporting_bp = Blueprint('reporting', __name__)

@reporting_bp.route('/summary')
def summary():
    """Provides a summarized report view."""
    # This route is namespaced as 'reporting.summary'
    return jsonify({
        "report_id": "RPT-2024-001",
        "total_records": 4500,
        "status": "Report generated successfully using reporting blueprint."
    })

# --- 5. The Application Factory Function ---

def create_app(config_name='default'):
    """
    The Flask Application Factory.
    Creates and configures a new Flask application instance dynamically.
    """
    # 5.1 Initialize the core Flask application
    app = Flask(__name__)

    # 5.2 Load configuration from the specified class
    app.config.from_object(config_map[config_name])

    # 5.3 Initialize extensions (logging, DB, etc.)
    init_extensions(app)

    # 5.4 Register Blueprints
    # Core blueprint registered at the root '/'
    app.register_blueprint(core_bp)
    
    # Reporting blueprint registered with a URL prefix '/data'
    # This isolates all reporting routes under this namespace
    app.register_blueprint(reporting_bp, url_prefix='/data')
    
    # 5.5 Optional: Register a global error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"error": "Resource not found", "details": str(e)}), 404

    return app

# --- 6. Runtime Execution Example ---

if __name__ == '__main__':
    # Demonstrate creating two distinct, isolated application instances
    # 1. Development Instance
    dev_app = create_app('development')
    
    # 2. Production Instance (used only to check configuration differences)
    prod_app = create_app('production')

    print("--- 1. Development Instance Configuration Check ---")
    # Check loaded configuration
    print(f"Debug Mode: {dev_app.config['DEBUG']}")
    print(f"Database URI: {dev_app.config['DATABASE_URI']}")
    
    # Check URL resolution using url_for
    # Note: url_for requires the application context or instance for resolution
    with dev_app.app_context():
        core_url = url_for('core.index')
        report_url = url_for('reporting.summary')
        print(f"Core Index URL: {core_url}")
        # The reporting URL includes the prefix registered in the factory
        print(f"Report Summary URL: {report_url}") 
    
    print("\n--- 2. Production Instance Configuration Check ---")
    print(f"Debug Mode: {prod_app.config['DEBUG']}")
    print(f"Database URI: {prod_app.config['DATABASE_URI']}")
    
    # To run the development server:
    # dev_app.run(port=5000)
