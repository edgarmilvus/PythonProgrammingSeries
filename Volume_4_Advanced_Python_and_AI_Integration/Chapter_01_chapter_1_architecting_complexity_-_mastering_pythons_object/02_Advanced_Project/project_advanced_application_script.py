
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

import sys

# --- 1. Data Descriptor: ResourceLimiter ---
# This descriptor controls access, validation, and storage for resource attributes.
class ResourceLimiter:
    """
    A non-data descriptor that enforces type checking and range limits 
    on configuration attributes (e.g., CPU/Memory).
    """
    def __set_name__(self, owner, name):
        """Called at class creation time, sets up the private storage name."""
        self.public_name = name
        self.private_name = f'_{name}'

    def __get__(self, obj, objtype=None):
        """Retrieves the value from the instance's private storage."""
        if obj is None:
            return self
        # Access the value stored on the instance
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        """Validates and sets the value, enforcing constraints."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"[{self.public_name}] must be a positive integer.")
        
        # Enforce maximum limit (e.g., maximum server size)
        MAX_RESOURCE = 16
        if value > MAX_RESOURCE:
            raise ValueError(f"[{self.public_name}] limit exceeded. Max allowed: {MAX_RESOURCE}.")
            
        # Store the valid value in the designated private attribute
        setattr(obj, self.private_name, value)

# --- 2. Base Class: ConfigBase (MRO Terminus and Architectural Control) ---
class ConfigBase:
    """
    The foundational class for all service configurations. 
    Uses __slots__ for memory optimization and descriptors for state control.
    """
    # Use __slots__ to prevent dynamic attribute creation and reduce memory footprint
    __slots__ = ('_service_name', '_cpu_cores', '_memory_gb')
    
    # Apply the descriptor to controlled attributes
    cpu_cores = ResourceLimiter()
    memory_gb = ResourceLimiter() 

    def __init_subclass__(cls, **kwargs):
        """Hook executed whenever a class inherits from ConfigBase."""
        super().__init_subclass__(**kwargs)
        # Architectural enforcement: Ensure all configuration subclasses define a port
        if not hasattr(cls, 'DEFAULT_PORT'):
            raise TypeError(f"Subclass {cls.__name__} must define a mandatory 'DEFAULT_PORT' class attribute.")

    def __init__(self, service_name: str, cpu: int, memory: int):
        """Initializes the instance, triggering descriptor __set__ methods."""
        self._service_name = service_name
        # Assignment here triggers the ResourceLimiter.__set__()
        self.cpu_cores = cpu  
        self.memory_gb = memory 

    def __repr__(self):
        return (f"<{self.__class__.__name__} | Name: {self._service_name}, "
                f"CPU: {self.cpu_cores}, Mem: {self.memory_gb}GB, Port: {self.DEFAULT_PORT}>")

    # Define the MRO terminus setup method (required for super() calls to terminate)
    def setup(self):
        """The final step in the MRO chain."""
        print(f"[BASE] Configuration finalized for {self._service_name}.")

# --- 3. Mixins (Injecting Behavior and MRO Complexity) ---
class LoggingMixin:
    """Provides standard logging initialization functionality."""
    def setup(self):
        print(f"[LOGGING] Initializing standard logging for {self._service_name}.")
        # Crucial: Delegate the call up the MRO chain
        super().setup()

class CachingMixin:
    """Provides distributed caching setup functionality."""
    def setup(self):
        print(f"[CACHING] Setting up distributed cache layer and connection pools.")
        # Crucial: Delegate the call up the MRO chain
        super().setup()

# --- 4. Concrete Implementations (Testing MRO and Descriptors) ---

class APIServiceConfig(CachingMixin, LoggingMixin, ConfigBase):
    """Configuration for an API service, using two mixins."""
    DEFAULT_PORT = 8080
    
    def setup(self):
        """Specific setup for the API service."""
        print(f"[API] Starting HTTP listener setup on port {self.DEFAULT_PORT}.")
        # Continue the MRO chain resolution
        super().setup()
        
class DatabaseServiceConfig(LoggingMixin, ConfigBase):
    """Configuration for a database service, using one mixin."""
    DEFAULT_PORT = 5432
    
    def setup(self):
        """Specific setup for the Database service."""
        print(f"[DB] Connecting to persistent storage and ensuring replication.")
        # Continue the MRO chain resolution
        super().setup()

# --- 5. Execution and Testing ---

print("--- 1. Initializing API Service Configuration (Complex MRO Test) ---")
# The MRO for this class is: APIServiceConfig -> CachingMixin -> LoggingMixin -> ConfigBase -> object
api_config = APIServiceConfig("UserAuthService", cpu=4, memory=8)
print(api_config)
print("\n--- Running Setup Chain (MRO Execution) ---")
api_config.setup()

print("\n--- 2. Initializing Database Service Configuration (Simple MRO Test) ---")
db_config = DatabaseServiceConfig("PostgresCluster", cpu=12, memory=16)
print(db_config)
print("\n--- Running Setup Chain (MRO Execution) ---")
db_config.setup()

print("\n--- 3. MRO Analysis (C3 Linearization Verification) ---")
# Display the actual MRO tuple calculated by C3 linearization
print(f"APIServiceConfig MRO: {APIServiceConfig.__mro__}")

print("\n--- 4. Descriptor Enforcement Test (Validation Failure) ---")
try:
    # Attempt to assign a value that violates the ResourceLimiter constraint (max 16)
    api_config.cpu_cores = 20 
except ValueError as e:
    print(f"Descriptor Error Caught: {e}")
    
print("\n--- 5. __slots__ Check (Memory Optimization and State Lock) ---")
try:
    # Attempt to dynamically add a new attribute to the slotted object
    api_config.new_runtime_attr = "Should Fail"
except AttributeError as e:
    print(f"__slots__ Check: Successfully prevented dynamic attribute creation: {e}")

# --- 6. Architectural Enforcement Test (__init_subclass__ Failure) ---
print("\n--- 6. Architectural Enforcement Test (__init_subclass__ Failure) ---")
try:
    # This class fails the check in ConfigBase.__init_subclass__ because it lacks DEFAULT_PORT
    class FaultyConfig(ConfigBase):
        pass 
except TypeError as e:
    print(f"__init_subclass__ Check: Successfully enforced architecture: {e}")

