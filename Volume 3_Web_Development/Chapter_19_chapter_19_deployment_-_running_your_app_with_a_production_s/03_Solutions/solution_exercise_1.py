
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

import multiprocessing
import os

# 1. Binding: Use a Unix socket for efficient communication with Nginx
bind = 'unix:/tmp/gunicorn_app.sock'

# 2. Worker Calculation: Use the recommended formula (2 * CPU_Cores) + 1
# This ensures high concurrency while utilizing CPU resources optimally.
cpu_cores = multiprocessing.cpu_count()
workers = (cpu_cores * 2) + 1

# 3. Logging: Direct logs to stdout/stderr for easy capture by logging systems (e.g., systemd, Docker)
accesslog = '-' 
# Log format includes response time (%D) for performance monitoring
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" (Response Time: %Dµs)'

errorlog = '-' 
loglevel = 'info'

# Exercise 4 Requirement (Worker Timeout):
timeout = 30 

# Exercise 4 Requirement (Post-Fork Hook):
def post_fork(server, worker):
    """
    Called just after a worker has been forked.
    Used for initializing worker-specific resources.
    """
    worker.log.info(f"Worker {os.getpid()} successfully forked and initializing complex resources.")
    pass

# Example Execution Command:
# gunicorn -c gunicorn.conf.py wsgi:application
