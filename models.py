"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
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