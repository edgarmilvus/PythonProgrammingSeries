
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

# Source File: solution_exercise_3.py
# Description: Solution for Exercise 3
# ==========================================

import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

# Setup
engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# 1. Model Modification
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return (f"User(id={self.id}, username='{self.username}', "
                f"deleted={self.is_deleted}, deleted_at={self.deleted_at})")

Base.metadata.create_all(engine)

# Initial Data
session = Session()
user_a = User(username="user_alpha")
user_b = User(username="user_beta")
session.add_all([user_a, user_b])
session.commit()
session.close()

# 2. Soft Delete Function (Update)
def soft_delete_user(user_id):
    session = Session()
    user = session.get(User, user_id)
    if user:
        if not user.is_deleted:
            user.is_deleted = True
            user.deleted_at = datetime.datetime.now()
            session.commit()
            print(f"Soft deleted User ID {user_id} ({user.username}). Deleted at: {user.deleted_at.strftime('%Y-%m-%d %H:%M')}")
        else:
            print(f"User ID {user_id} already soft deleted.")
    else:
        print(f"User ID {user_id} not found.")
    session.close()

# 3. Hard Delete (Purge) Function (Delete)
def purge_old_users(days_old):
    session = Session()
    # Calculate the cutoff date
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_old)
    
    print(f"\n--- PURGE Operation: Searching for users deleted before {cutoff_date.strftime('%Y-%m-%d')} ({days_old} days old) ---")

    # Query for users marked as deleted AND older than the cutoff
    users_to_purge = session.query(User).filter(
        User.is_deleted == True,
        User.deleted_at < cutoff_date
    ).all()

    if not users_to_purge:
        print("No users found matching the purge criteria.")
        session.close()
        return

    count = 0
    for user in users_to_purge:
        print(f"Purging user: {user.username} (Soft deleted on: {user.deleted_at})")
        session.delete(user)
        count += 1
    
    session.commit()
    print(f"Successfully purged {count} user(s).")
    session.close()

# 4. Execution and 5. Verification
print("--- Initial State ---")
session = Session()
print(session.query(User).all())
session.close()

# b. Soft deleting User 1
soft_delete_user(1)

# c. Attempting to purge users older than 1 day (should find 0)
purge_old_users(days_old=1)

# d. Manually setting User 2's deleted_at to 10 days in the past (must reopen session)
session = Session()
user2 = session.get(User, 2)
if user2:
    user2.is_deleted = True
    user2.deleted_at = datetime.datetime.now() - datetime.timedelta(days=10)
    session.commit()
    print(f"\nManually set User 2's deletion date to 10 days ago: {user2.deleted_at}")
session.close()

# e. Purging users older than 1 day (should only purge User 2)
purge_old_users(days_old=1)

# Final Verification
session = Session()
print("\n--- Final State Verification ---")
print(session.query(User).all())
session.close()
