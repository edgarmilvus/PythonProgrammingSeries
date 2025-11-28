
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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, select
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Setup
engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# 1. Model Setup
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    major = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    enrollments = relationship("CourseEnrollment", back_populates="student")

    def __repr__(self):
        return f"Student(name='{self.name}', major='{self.major}', active={self.is_active})"

class CourseEnrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_code = Column(String)
    grade = Column(String) # e.g., 'A', 'B', 'C', 'F'

    student = relationship("Student", back_populates="enrollments")

# Create tables
Base.metadata.create_all(engine)

# 2. Data Population
def populate_university_data(session):
    students = [
        Student(name="Alice Johnson", major="Computer Science", is_active=True),
        Student(name="Bob Smith", major="Physics", is_active=True),
        Student(name="Charlie Brown", major="Computer Science", is_active=False), # Inactive
        Student(name="Diana Prince", major="Computer Science", is_active=True),
        Student(name="Eve Adams", major="Computer Science", is_active=True), # Has an 'F' grade
    ]
    session.add_all(students)
    session.flush() # Assign IDs before enrollments

    enrollments = [
        # Alice (CS, Active, All good grades) -> Should qualify
        CourseEnrollment(student_id=students[0].id, course_code="CS101", grade='A'),
        CourseEnrollment(student_id=students[0].id, course_code="MATH202", grade='B'),

        # Bob (Physics, Active) -> Fails Major filter
        CourseEnrollment(student_id=students[1].id, course_code="PHYS300", grade='A'),

        # Charlie (CS, Inactive) -> Fails Active filter
        CourseEnrollment(student_id=students[2].id, course_code="CS101", grade='A'),

        # Diana (CS, Active, Mixed grades but no F) -> Should qualify
        CourseEnrollment(student_id=students[3].id, course_code="CS202", grade='B'),
        CourseEnrollment(student_id=students[3].id, course_code="ENG100", grade='C'),

        # Eve (CS, Active, Has an F) -> Fails Exclusion filter
        CourseEnrollment(student_id=students[4].id, course_code="CS305", grade='A'),
        CourseEnrollment(student_id=students[4].id, course_code="MATH101", grade='F'),
    ]
    session.add_all(enrollments)
    session.commit()

session = Session()
populate_university_data(session)

# 3. Honors Query Construction
# Step 1: Identify the IDs of all students who have at least one failing grade ('F').
failing_student_ids_subquery = select(CourseEnrollment.student_id).where(
    CourseEnrollment.grade == 'F'
).distinct()

# Step 2: Construct the main query using exclusion and filtering.
honors_students = session.scalars(
    select(Student.name)
    .where(
        # a. Must be active
        Student.is_active == True,
        # b. Must be in Computer Science major
        Student.major == 'Computer Science',
        # c. Must NOT be in the list of students with failing grades (Exclusion)
        Student.id.not_in(failing_student_ids_subquery)
    )
    # d. Order alphabetically
    .order_by(Student.name)
).all()

# 4. Execution and Output
print("--- Honors List Report ---")
if honors_students:
    for name in honors_students:
        print(f"- {name}")
else:
    print("No students meet all honors criteria.")

session.close()
