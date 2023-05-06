"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, LargeBinary
from sqlalchemy.orm import relationship
from database import Base

# TODO: Complete your models
class User(Base):
    __tablename__ = "users"

    id = Column("id", INTEGER, primary_key=True)
    email = Column("email", TEXT)
    password = Column("password", TEXT, nullable=False)

    def __init__(self, email, password, id=None):
        print("initialized!")
        self.id = id
        self.email = email
        self.password = password

    def __repr__(self):
        return self.email
    
class Submission(Base):
    __tablename__ = "Submissions"

    id = Column("id", INTEGER, primary_key = True)
    donor_age = Column("donor_age", INTEGER)
    percent_steatosis = Column("percent_steatosis", INTEGER)
    other_info = Column("other_info", TEXT)
    file = Column("file", LargeBinary, nullable=False)

    def __init__(self, donor_age, percent_steatosis, other_info, file):
        self.donor_age = donor_age
        self.percent_steatosis = percent_steatosis
        self.other_info = other_info 
        self.file = file