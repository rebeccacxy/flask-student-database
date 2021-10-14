# main.py

from app import app
from db_setup import init_db, db_session
from forms import StudentSearchForm, StudentForm, ScoreForm
from flask import flash, render_template, request, redirect, url_for, make_response
from models import Student, Score
from tables import Results, Score_Results
import csv
import os

init_db()

uploads_dir = 'uploads'
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

@app.route('/', methods=['GET', 'POST'])
def index():
    search = StudentSearchForm(request.form)
    if request.method == 'POST':
        if request.files:
            file = request.files['filename']
            file.save(os.path.join(uploads_dir, file.filename))

        return search_results(search)

    return render_template('index.html', form=search)

# Get the uploaded files
@app.route("/upload")
def uploadFiles():
    if request.method == 'POST':
        # get the uploaded file
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
    # save the file
    return redirect(url_for('index'))


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Student':
            qry = db_session.query(Student).filter(Student.name.contains(search_string))
            results = qry.all()
            qryscore = db_session.query(Score)
            score_results = qryscore.all()
        elif search.data['select'] == 'Score':
            qry = db_session.query(Student)
            results = qry.all()
            qry_score = db_session.query(Score).filter(Score.name.contains(search_string))
            score_results = qry_score.all()
    else:
        qry = db_session.query(Student)
        qryscore = db_session.query(Score)
        results = qry.all()
        score_results = qryscore.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = Results(results)
        table.border = True
        table2 = Score_Results(score_results)
        table2.border = True
        return render_template('results.html', table=table, table2=table2)


@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    """
    Add a new student
    """
    form = StudentForm(request.form)

    if request.method == 'POST' and form.validate():
        # save the student
        student = Student()
        save_changes(student, form, new=True)
        flash('Student added successfully!')
        return redirect('/')

    return render_template('new_student.html', form=form)

@app.route('/new_score', methods=['GET', 'POST'])
def new_score():
    """
    Add a new student
    """
    form = ScoreForm(request.form)

    if request.method == 'POST' and form.validate():
        # save the student
        score = Score()
        save_changes_toscore(score, form, new=True)
        flash('Score added successfully!')
        return redirect('/')

    return render_template('new_score.html', form=form)


def save_changes(student, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object

    student.name = form.name.data
    student.password = form.password.data
    student.student_class = form.student_class.data

    if new:
        # Add the new student to the database
        db_session.add(student)

    # commit the data to the database
    db_session.commit()

def save_changes_toscore(score, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object

    score.id = len(db_session.query(Score).all()) + 1
    score.name = form.name.data
    score.subject = form.subject.data
    score.score = form.score.data

    if new:
        # Add the new student to the database
        db_session.add(score)

    # commit the data to the database
    db_session.commit()


@app.route('/edit_student/<string:name>', methods=['GET', 'POST'])
def edit(name):
    """
    Add / edit an item in the database
    """
    qry = db_session.query(Student).filter(Student.name==name)
    student = qry.first()

    if student:
        form = StudentForm(formdata=request.form, obj=student)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(student, form)
            flash('Student updated successfully!')
            return redirect('/')
        return render_template('edit_student.html', form=form)
    else:
        return 'Error loading #{name}'.format(name=name)

@app.route('/edit_score/<int:id>', methods=['GET', 'POST'])
def edit_score(id):
    """
    Add / edit an item in the database
    """
    qry = db_session.query(Score).filter(Score.id==id)
    score = qry.first()

    if score:
        form = ScoreForm(formdata=request.form, obj=score)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes_toscore(score, form)
            flash('Score updated successfully!')
            return redirect('/')
        return render_template('edit_score.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


@app.route('/delete/<string:name>', methods=['GET', 'POST'])
def delete(name):
    """
    Delete the item in the database that matches the specified
    id in the URL
    """
    qry = db_session.query(Student).filter(
        Student.name == name)
    student = qry.first()

    if student:
        form = StudentForm(formdata=request.form, obj=student)
        if request.method == 'POST' and form.validate():
            # delete the item from the database
            db_session.delete(student)
            db_session.commit()

            flash('Student deleted successfully!')
            return redirect('/')
        return render_template('delete_student.html', form=form)
    else:
        return 'Error deleting #{name}'.format(name=name)

@app.route('/delete_score/<string:name>', methods=['GET', 'POST'])
def delete_score(name):
    """
    Delete the item in the database that matches the specified
    id in the URL
    """
    qry = db_session.query(Score).filter(
        Score.name == name)
    score = qry.first()

    if score:
        form = ScoreForm(formdata=request.form, obj=score)
        if request.method == 'POST' and form.validate():
            # delete the item from the database
            db_session.delete(score)
            db_session.commit()

            flash('Score deleted successfully!')
            return redirect('/')
        return render_template('delete_score.html', form=form)
    else:
        return 'Error deleting #{name}'.format(name=name)

@app.route('/download_student/')
def download_csv():
    output_dir = os.path.join('output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join('output', "output.csv"), 'w') as csvfile:

        fieldnames = ['name', 'password', 'student_class']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        q1 = db_session.query(Student).all()

        rows = []
        for row in q1:
            rows.append(
                {
                    'name': row.name,
                    'password': row.password,
                    'student_class': row.student_class
                }
            )

        for row in rows:
            writer.writerow(dict(
                (k, v) for k, v in row.items()
            ))
        csvfile.close()

    return "CSV file has been downloaded"

@app.route('/download_score/')
def download_csv_score():
    output_dir = os.path.join('output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join('output', "output.csv"), 'w') as csvfile:

        fieldnames = ['name', 'subject', 'score']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        q1 = db_session.query(Score).all()

        rows = []
        for row in q1:
            rows.append(
                {
                    'name': row.name,
                    'subject': row.subject,
                    'score': row.score
                }
            )

        for row in rows:
            writer.writerow(dict(
                (k, v) for k, v in row.items()
            ))
        csvfile.close()

    return "CSV file has been downloaded"

if __name__ == '__main__':
    import os
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = False
    app.run(port=5001, debug=True)