from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Textbook(Base):
    __tablename__ = "textbooks"
    id = Column(Integer, primary_key=True, index=True)
    grade = Column(String, index=True)
    subject = Column(String, index=True)
    curriculum = Column(String, index=True)
    content = Column(String)