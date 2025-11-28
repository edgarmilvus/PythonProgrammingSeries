
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
import shutil
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from alembic.config import Config
from alembic import command

# --- 1. Configuration and Setup ---

# Use an in-memory SQLite database for demonstration
DATABASE_URL = "sqlite:///./alembic_test.db"
ALEMBIC_DIR = "migrations_env"
Base = declarative_base()

# --- 2. Define Initial Model (V1) ---

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    # V1 column name
    status = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

# --- 3. Programmatic Alembic Manager Class ---

class AlembicConfigurator:
    """
    Manages Alembic configuration and command execution programmatically.
    This replaces manual command-line interaction for automation.
    """
    def __init__(self, db_url, alembic_dir, metadata):
        self.db_url = db_url
        self.alembic_dir = alembic_dir
        self.metadata = metadata
        self.config = None

    def _prepare_config(self):
        """Loads and prepares the Alembic configuration object."""
        # Create a basic Alembic configuration object
        cfg = Config()
        
        # Set the location of the environment scripts
        cfg.set_main_option("script_location", self.alembic_dir)
        
        # Set the database URL for the 'env.py' script to use
        cfg.set_main_option("sqlalchemy.url", self.db_url)
        
        # Store the SQLAlchemy metadata object directly in the config context
        # This is how 'env.py' knows which models to compare against the database
        cfg.attributes['target_metadata'] = self.metadata
        self.config = cfg

    def init_environment(self):
        """Initializes the migration environment (simulates 'alembic init')."""
        if Path(self.alembic_dir).exists():
            shutil.rmtree(self.alembic_dir)
            print(f"# Cleaned up existing directory: {self.alembic_dir}")
        
        # Use the standard 'generic' template for initialization
        command.init(self.config, self.alembic_dir, type='generic')
        print(f"# Alembic environment initialized at: {self.alembic_dir}")

    def stamp_head(self):
        """Stamps the database to the 'head' revision (used for fresh start)."""
        self._prepare_config()
        # Stamps the database schema version table without running migrations
        command.stamp(self.config, "head")
        print("# Database stamped to 'head' revision.")

    def generate_revision(self, message):
        """
        Generates a new migration script, using autogenerate based on metadata changes.
        """
        self._prepare_config()
        # The 'autogenerate=True' flag is crucial; it compares target_metadata 
        # against the current database schema
        command.revision(self.config, message=message, autogenerate=True)
        print(f"# Generated new revision: '{message}'")
        
    def upgrade(self, revision='head'):
        """Applies migrations up to the specified revision."""
        self._prepare_config()
        print(f"# Applying upgrade to revision: {revision}")
        command.upgrade(self.config, revision)
        print("# Upgrade complete.")

# --- 4. Execution Flow ---

def run_migration_lifecycle():
    # 4.1 Initial Setup (V1)
    print("--- Phase 1: Initial Setup (Model V1) ---")
    
    # Initialize DB engine and create tables based on V1 model
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine) 
    print("# Database initialized with V1 schema.")

    # Instantiate the Alembic Manager
    alembic_manager = AlembicConfigurator(DATABASE_URL, ALEMBIC_DIR, Base.metadata)
    alembic_manager._prepare_config() # Pre-load config for init/stamp

    # Initialize environment and stamp the DB as if V1 was manually created
    alembic_manager.init_environment()
    alembic_manager.stamp_head()

    # 4.2 Schema Evolution (V2)
    print("\n--- Phase 2: Schema Evolution (Model V2) ---")
    
    # 4.2a Define the schema change (Monkey Patching the model)
    # In a real application, you would modify the source model file directly.
    
    # 1. Rename 'status' to 'is_active' (requires explicit rename logic in migration script)
    # Note: Alembic autogenerate struggles with renames, but detects the drop/add.
    # For this demo, we simulate the *desired* V2 state in the Python model:
    del User.status # Remove old attribute
    User.is_active = Column('status', Boolean, default=True, nullable=False) # Keep old column name temporarily for autogenerate detection
    
    # 2. Add a new required column 'role'
    User.role = Column(String(20), nullable=False, server_default='user')
    
    # 4.2b Generate Migration Script
    # Alembic compares Base.metadata (which now contains V2) against the DB schema (V1)
    alembic_manager.generate_revision("Add role and rename status")

    # 4.3 Applying the Migration
    print("\n--- Phase 3: Applying Migration ---")
    alembic_manager.upgrade()

    # 4.4 Verification (Optional cleanup)
    print("\n--- Phase 4: Verification and Cleanup ---")
    # Verify the table structure (requires manual inspection of the DB or SQL queries)
    
    # Clean up the generated files
    shutil.rmtree(ALEMBIC_DIR)
    os.remove(Path(DATABASE_URL).name)
    print("# Cleanup complete. Database and migration environment removed.")

if __name__ == "__main__":
    run_migration_lifecycle()
