
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
from flask import Flask
from dotenv import load_dotenv

# --- 1. CONFIGURATION CLASSES (Simulating config.py) ---

class BaseConfig:
    """Base configuration class containing settings common to all environments."""
    # The secret key MUST be loaded from the OS environment for production security.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-insecure-dev-key')
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Define a placeholder for the database URL
    SQLALCHEMY_DATABASE_URI = None

class DevelopmentConfig(BaseConfig):
    """Development configuration: Enables debug mode and uses a local SQLite DB."""
    DEBUG = True
    # Use a simple relative path SQLite DB for convenience
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'dev_db.sqlite3'
    )
    # Allows printing config status during startup
    print("--- Running in DEVELOPMENT Mode ---")

class ProductionConfig(BaseConfig):
    """Production configuration: Disables debug mode and requires external DB URI."""
    DEBUG = False
    # Set a high log level for production
    LOG_LEVEL = 'WARNING'

    # CRITICAL: Production must use a securely provided external database URI.
    # We enforce that the environment variable MUST be present.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    if SQLALCHEMY_DATABASE_URI is None:
        # Fail fast if a required production setting is missing
        raise EnvironmentError(
            "FATAL: DATABASE_URL environment variable is not set for ProductionConfig."
        )

    print("--- Running in PRODUCTION Mode ---")

# Mapping the environment string to the configuration class
CONFIG_MAPPING = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': BaseConfig # Placeholder for testing config
}

# --- 2. APPLICATION FACTORY (Simulating __init__.py) ---

def create_app(config_name='development'):
    """
    The Application Factory function.
    Initializes and configures the Flask application instance dynamically.
    """
    # 2.1 Instantiate the core Flask application
    app = Flask(__name__)

    # 2.2 Select the appropriate configuration class
    config_class = CONFIG_MAPPING.get(config_name, DevelopmentConfig)
    
    # 2.3 Apply configuration settings to the app instance
    app.config.from_object(config_class)

    # 2.4 Register a simple route/blueprint (for demonstration)
    @app.route('/')
    def index():
        db_status = f"DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}"
        debug_status = f"Debug Mode: {app.config['DEBUG']}"
        env_status = f"Environment: {config_name.upper()}"
        
        return f"<h1>Configuration Status Check</h1><p>{env_status}</p><p>{debug_status}</p><p>{db_status}</p>"

    return app

# --- 3. RUNNER SCRIPT (Simulating app.py) ---

def run_server():
    """
    Main execution function that loads environment variables and starts the app.
    """
    # 3.1 Load environment variables from .env file for local development convenience.
    # This call is silently ignored in production environments where variables 
    # are managed by the host (e.g., Gunicorn/Docker/Kubernetes).
    load_dotenv()

    # 3.2 Determine the environment. Default to 'development' if not set.
    # We normalize the environment variable key to lowercase for mapping consistency.
    env_name = os.environ.get('FLASK_ENV', 'development').lower()

    # 3.3 Ensure the environment name is valid
    if env_name not in CONFIG_MAPPING:
        print(f"Warning: Unknown environment '{env_name}'. Defaulting to 'development'.")
        env_name = 'development'

    # 3.4 Create the configured application instance
    application = create_app(env_name)

    # 3.5 Run the application (This line would typically be replaced by Gunicorn 
    # in a production setting, which calls the 'application' object directly).
    # For local testing, we use the built-in server.
    if env_name == 'development':
        application.run(host='0.0.0.0', port=5000)
    else:
        # In a real scenario, this block would log instructions for Gunicorn setup.
        print("\n--- Production Ready ---")
        print("To run in production, use a WSGI server like Gunicorn:")
        print(f"gunicorn -w 4 'app:application' --env FLASK_ENV={env_name}")

# Execute the main function
if __name__ == '__main__':
    # Set dummy environment variables for demonstration purposes if they don't exist
    # In a real setup, these would be in the .env file or OS environment
    if 'SECRET_KEY' not in os.environ:
        os.environ['SECRET_KEY'] = 'a-secure-secret-key-from-os'
        
    # Example: To test production mode, uncomment the line below and ensure 
    # DATABASE_URL is set (e.g., in a separate .env file or terminal export).
    # os.environ['FLASK_ENV'] = 'production' 
    # os.environ['DATABASE_URL'] = 'postgresql://user:pass@host:5432/prod_db'
    
    run_server()
