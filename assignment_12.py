#!user/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, session, g, url_for, flash
import sqlite3
from contextlib import closing

DATABASE = 'hw12.db'
SECRET_KEY = 'secret_key'
USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def get_db():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect('/dashboard')
    return render_template('login.html', error=error)

@app.route('/dashboard', methods = ['GET'])
def dashboard():
    if session['logged_in'] == False:
        return redirect('/login')
    else:
        #return render_template('dashboard.html')
        cur = g.db.execute('SELECT id, first_name, last_name FROM students order by id')
        students = [dict(id=row[0], first_name=row[1], last_name=row[2]) for row in cur.fetchall()]
        #print students
        cur2 = g.db.execute('SELECT id, subject, num_questions, date FROM quizzes order by id')
        quizzes = [dict(id=row[0], subject=row[1], num_questions=row[2], date=row[3]) for row in cur2.fetchall()]
        return render_template('dashboard.html', students = students, quizzes = quizzes)

@app.route('/student/add', methods = ['GET', 'POST'])
def add_student():
    try:
        if session['logged_in'] == False:
            return redirect('/login')
        else:
            if request.method == 'GET':
                return render_template('add_students.html')

            if request.method == 'POST':
                g.db.execute("INSERT INTO students (first_name, last_name) VALUES (?, ?)",
                             [request.form['first_name'], request.form['last_name']])
                g.db.commit()
    except:
        print 'error'
        render_template('add_students.html')
    return redirect('/dashboard')

@app.route('/quiz/add', methods = ['GET', 'POST'])
def add_quiz():
    if session['logged_in'] == False:
        return redirect('/login')
    else:
        if request.method == 'GET':
            return render_template('add_quizzes.html')

        if request.method == 'POST':
            g.db.execute("INSERT INTO quizzes (subject, num_questions, date) VALUES (?, ?, ?)",
                        [request.form['subject'], request.form['num_questions'], request.form['date']])
        g.db.commit()
    return redirect('/dashboard')

@app.route('/add_results/add', methods = ['GET'])
#not working yet
def student_grades():
    return render_template('results.html')
    if session['logged_in'] == False:
        return redirect('/login')
    cur = g.db.execute("SELECT first_name, last_name FROM students WHERE id=?", id)
    print cur
    #, quizzes.subject, results.score FROM students INNER JOIN results ON students.id = results.student_id INNER JOIN quizzes  ON quizzes.id  = results.quiz_id WHERE students.id = ?', id)
    student_results = [dict(first_name=row[0], last_name=row[1], subject=row[2], grade=row[3]) for row in cur.fetchall()]
    return render_template('add_results.html')#, student_results = student_results)

@app.route('/add_results/add', methods = ['GET', 'POST'])
def result():
    print 'results'
    if session['logged_in'] == False:
        return redirect('/login')

    if request.method == 'GET':
        #return render_template('results.html')
        cur = g.db.execute("SELECT id, first_name, last_name FROM students ORDER BY id")
        students = [dict(id=row[0], first_name=row[1], last_name=row[2]) for row in cur.fetchall()]
        cur2 = g.db.execute("SELECT id, subject FROM quizzes ORDER BY id")
        quizzes = [dict(id=row[0], subject=row[1]) for row in cur2.fetchall()]
        #print students, quizzes
        return render_template('results.html', students = students, quizzes = quizzes)

    if request.method == 'POST':
        print'post'
        g.db.execute("INSERT INTO results (students, quizzes, score) VALUES (?, ?, ?)",
                     [request.form['add_student'], request.form['add_quiz'], request.form['add_score']])
        g.db.commit()
        return redirect('/dashboard')

if __name__ == "__main__":
    app.run(debug = True)
    connect_db()
