
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

class CMSPage(Base):
    __tablename__ = 'cms_page'
    
    # 1. Primary Key
    id = Column(Integer, primary_key=True)
    
    # 2. URL Slug: Unique and Non-nullable
    slug = Column(String(128), unique=True, nullable=False)
    
    # 3. Content Body: Use Text for large content
    content = Column(Text)
    
    # 6. Status Flag
    is_published = Column(Boolean, default=False)
    
    # 5. Timestamps (using datetime.utcnow for timezone-agnostic storage)
    created_at = Column(DateTime, default=datetime.utcnow)
    # The onupdate argument ensures the column is updated on every modification 
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 

    def __repr__(self):
        return f"<CMSPage(slug='{self.slug}', published={self.is_published})>"
