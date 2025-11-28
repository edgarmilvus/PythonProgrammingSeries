
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

# Source File: solution_exercise_8.py
# Description: Solution for Exercise 8
# ==========================================

def upgrade():
    # 1. Add a new, temporary column with the desired type and name, allowing NULLs initially.
    op.add_column('users', sa.Column('contact_email_temp', sa.String(255), nullable=True))

    # 2. Copy data from the old column to the new column.
    # This ensures data is preserved even if the next steps fail.
    op.execute("UPDATE users SET contact_email_temp = email")

    # 3. Drop the old column.
    op.drop_column('users', 'email')

    # 4. Rename the temporary column to the final name.
    op.rename_column('users', 'contact_email_temp', 'contact_email')
    
    # 5. Alter the column to enforce the final constraints (e.g., non-nullable).
    # This step should only be done after data copy is complete.
    op.alter_column('users', 'contact_email', nullable=False, existing_type=sa.String(255)) 
