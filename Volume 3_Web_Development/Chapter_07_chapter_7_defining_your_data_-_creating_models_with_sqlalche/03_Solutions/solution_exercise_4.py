
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

# Source File: solution_exercise_4.py
# Description: Solution for Exercise 4
# ==========================================

class Department(Base):
    __tablename__ = 'department'

    # 1. Department Definition
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    # 3. Establish Relationship (One side)
    # backref creates the 'employee.department' attribute
    # cascade ensures related employees are handled upon department deletion
    employees = relationship(
        "Employee", 
        backref="department", 
        cascade="all, delete-orphan", 
        lazy="dynamic"  # Use lazy="dynamic" for efficient querying of large lists
    )

    def __repr__(self):
        return f"<Department(name='{self.name}')>"

class Employee(Base):
    __tablename__ = 'employee'

    # 2. Employee Definition
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    # Foreign Key definition referencing the department table
    department_id = Column(Integer, ForeignKey('department.id')) 

    def __repr__(self):
        return f"<Employee(name='{self.name}', dept_id={self.department_id})>"
