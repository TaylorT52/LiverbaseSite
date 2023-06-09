"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, LargeBinary, DOUBLE
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"

    email = Column("email", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)
    submissions = relationship("Submission", back_populates="user")

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return self.email
    
class Submission(Base):
    __tablename__ = "submission"

    submission_id = Column("submission_id", INTEGER, primary_key = True)
    donor_age = Column("donor_age", INTEGER)
    percent_steatosis = Column("percent_steatosis", INTEGER)
    other_info = Column("other_info", TEXT)
    file = Column("file", LargeBinary, nullable=False)

    user_id = Column("user_id", ForeignKey("user.email"))
    user = relationship("User", back_populates="submissions")

    result = relationship("Result", cascade="all, delete-orphan", back_populates="submission")

    def __init__(self, user_id, donor_age, percent_steatosis, other_info, file):
        self.donor_age = donor_age
        self.percent_steatosis = percent_steatosis
        self.other_info = other_info 
        self.file = file
        self.user_id = user_id

class Result(Base):
    __tablename__ = "result"

    submission_id = Column("submission_id", ForeignKey("submission.submission_id"), primary_key=True)
    submission = relationship("Submission", back_populates="result")

    percent_steatosis = Column("percent_steatosis", DOUBLE)
    mask = Column("mask", LargeBinary)

    def __init__(self, submission_id, percent_steatosis, mask):
        self.submission_id = submission_id
        self.percent_steatosis = percent_steatosis 
        self.mask = mask
