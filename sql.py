import sqlite3

with sqlite3.connect("hw12.db") as connection:
	c = connection.cursor()
	c.execute("""DROP TABLE students""")
	c.execute("""DROP TABLE results""")
	c.execute("""DROP TABLE quizzes""")

	c.execute("""CREATE TABLE students(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL)""")

	c.execute("""CREATE TABLE quizzes(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	subject TEXT,
	num_questions INTEGER,
	date TEXT)""")

	c.execute("""CREATE TABLE results(
	student_id INTEGER NOT NULL,
	quiz_id INTEGER NOT NULL,
	score INT)""")
	c.execute('INSERT INTO students (id, first_name, last_name) values (1, "John", "Smith")')
	c.execute('INSERT INTO quizzes (id, subject, num_questions, date) values (1, "Python Basics", 5, "February, 5th, 2015")')
	c.execute('INSERT INTO RESULTS (student_id, quiz_id, score) values (1,001,85)')
