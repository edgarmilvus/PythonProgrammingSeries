
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

INVENTORY_DATA = {
    "SKU-4815": {"name": "Laptop Pro 15", "stock": 12, "price": 1299.99},
    "SKU-1623": {"name": "Monitor Ultra 4K", "stock": 5, "price": 450.00},
    "SKU-4299": {"name": "Keyboard Mechanical", "stock": 25, "price": 110.50}
}
SENSOR_READINGS = [
    {"timestamp": "2023-10-26T10:00:00Z", "temp_c": 21.5, "humidity": 65},
    {"timestamp": "2023-10-26T10:05:00Z", "temp_c": 22.1, "humidity": 64},
    {"timestamp": "2023-10-26T10:10:00Z", "temp_c": "ERROR", "humidity": 66},
    {"timestamp": "2023-10-26T10:15:00Z", "temp_c": 23.0, "humidity": 68}
]
DEFAULT_CONFIG = {
    "logging": {"level": "INFO", "format": "%(asctime)s - %(message)s"},
    "network": {"timeout": 30, "retries": 3},
    "security": {"enabled": True}
}
USER_CONFIG = {
    "logging": {"level": "DEBUG"},
    "network": {"retries": 5, "protocol": "HTTPS"},
    "database": {"host": "localhost"}
}
API_USERS_DATA = [
    {"user_id": 101, "name_first": "Alice", "name_last": "Smith", "status_code": "A"},
    {"user_id": 102, "name_first": "Bob", "name_last": "Johnson", "status_code": "I"},
    {"user_id": 103, "name_first": "Charlie", "name_last": "Brown", "status_code": "A"}
]
