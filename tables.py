from flask_table import Table, Col, LinkCol

class Results(Table):
    id = Col('Id', show=False)
    # student = Col('Student')
    name = Col('Name')
    password = Col('Password')
    student_class = Col('Student_Class')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(name='name'))
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(name='name'))

class Score_Results(Table):
    id = Col('Id', show=False)
    name = Col('Name')
    subject = Col('Subject')
    score = Col('Score')
    edit = LinkCol('Edit', 'edit_score', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_score', url_kwargs=dict(name='name'))