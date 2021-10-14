# forms.py

from wtforms import Form, StringField, SelectField, validators

class StudentSearchForm(Form):
    choices = [('Student', 'Student'),
               ('Score', 'Score')]
    select = SelectField('Search for Student name:', choices=choices)
    search = StringField('')


class StudentForm(Form):
    name = StringField('Name')
    password = StringField('Password')
    student_class = StringField('Student_Class')


class ScoreForm(Form):
    name = StringField('Name')
    subject = StringField('Subject')
    score = StringField('Score')
