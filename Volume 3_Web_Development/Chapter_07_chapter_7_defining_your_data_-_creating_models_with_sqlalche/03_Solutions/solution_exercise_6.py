
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

# Source File: solution_exercise_6.py
# Description: Solution for Exercise 6
# ==========================================

# 1. Define the Association Table (using Table construct and metadata)
document_tag_association = Table(
    'document_tag_association', 
    metadata,
    # Define document_id as FK and part of the composite PK
    Column('document_id', Integer, ForeignKey('document.id'), primary_key=True),
    # Define tag_id as FK and part of the composite PK
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True),
    # The composite PK ensures a document can only have a specific tag once.
)

# 2. Define Document Model
class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))

    # 4. Conceptual Relationship Definition (using 'secondary' argument)
    # tags = relationship("Tag", secondary=document_tag_association, back_populates="documents")

    def __repr__(self):
        return f"<Document(title='{self.title}')>"

# 3. Define Tag Model
class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    # 4. Conceptual Relationship Definition (using 'secondary' argument)
    # documents = relationship("Document", secondary=document_tag_association, back_populates="tags")

    def __repr__(self):
        return f"<Tag(name='{self.name}')>"
