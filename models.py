from app import db
import pandas as pd
from pathlib import Path
import os

class Student(db.Model):
    __tablename__ = "students"
    engine = db.get_engine()

    if Path('uploads').is_dir() and len(os.listdir("uploads")) > 0 and [file.startswith("student") for file in os.listdir("uploads")]:
        # Read CSV with Pandas
        filename = [filename for filename in os.listdir('.') if filename.startswith("student")][0]
        with open(os.path.join('uploads', filename), 'r') as file:
            df = pd.read_csv(file)
    else:
        csv_file_path = "student1.csv"
        with open(csv_file_path, 'r') as file:
            df = pd.read_csv(file)

    # Insert to DB
    df.to_sql(name=__tablename__,
              con=engine,
              index=True,
              index_label='id',
              if_exists='replace')

    id = db.Column(db.Integer)
    name = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    student_class = db.Column(db.String)

    def __repr__(self):
        return "{}".format(self.name)


class Score(db.Model):
    __tablename__ = "scores"
    engine = db.get_engine()  # db is the one from the question

    if Path('uploads').is_dir() and len(os.listdir("uploads")) > 0 and [file.startswith("mark") for file in os.listdir("uploads")]:
        filename = [filename for filename in os.listdir('.') if filename.startswith("mark")][0]
        # Read CSV with Pandas
        with open(os.path.join('uploads', filename), 'r') as file:
            df = pd.read_csv(file)
    else:
        csv_file_path = "mark1.csv"
        # Read CSV with Pandas
        with open(csv_file_path, 'r') as file:
            df = pd.read_csv(file)

    # Insert to DB
    df.to_sql(name=__tablename__,
              con=engine,
              index=True,
              index_label='id',
              if_exists='replace')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    subject = db.Column(db.String)
    score = db.Column(db.String)

    def __repr__(self):
        return "{}".format(self.name)

