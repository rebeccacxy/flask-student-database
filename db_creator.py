from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///mystudent.db', echo=True)
Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer)
    name = Column(String, primary_key=True)
    password = Column(String)
    student_class = Column(String)

    def __repr__(self):
        return "<Student: {}>".format(self.name)

class Score(Base):
    __tablename__ = "scores"
    # name,subject,score

    id = Column(Integer, primary_key=True)
    name = Column(String)
    subject = Column(String)
    score = Column(String)

    def __repr__(self):
        return "<Score: {}>".format(self.name)

# create tables
Base.metadata.create_all(engine)