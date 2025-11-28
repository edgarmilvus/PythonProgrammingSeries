
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

# Source File: solution_exercise_9.py
# Description: Solution for Exercise 9
# ==========================================

def downgrade():
    # 1. Add back the original column name and type, allowing NULLs temporarily.
    op.add_column('users', sa.Column('email_temp', sa.String(120), nullable=True))

    # 2. Copy data back from the current column to the temporary old column.
    # Data truncation may occur here if new data exceeds 120 characters, 
    # but this is the necessary step for a full revert.
    op.execute("UPDATE users SET email_temp = contact_email")

    # 3. Drop the new column.
    op.drop_column('users', 'contact_email')

    # 4. Rename the temporary column back to the original name.
    op.rename_column('users', 'email_temp', 'email')
    
    # 5. Alter the column to re-establish original constraints (if necessary, 
    # though the original definition should cover this).
    op.alter_column('users', 'email', nullable=False, existing_type=sa.String(120))
