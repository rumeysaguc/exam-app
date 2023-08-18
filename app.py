from flask import Flask, request, session
from flask import render_template
import psycopg2
import re
from flask_login import login_required


app = Flask(__name__)
app.debug = True
connection = psycopg2.connect(
    host="localhost",
    database="weather-forecast",
    user='postgres',
    password='1234')

@login_required
@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            postgres_insert_query = """ INSERT INTO accounts (USERNAME, PASSWORD, EMAIL) VALUES (%s, %s, %s) RETURNING ID"""
            record_to_insert = (username, password, email)
            cursor.execute(postgres_insert_query, record_to_insert)
            new_id = cursor.fetchone()[0]
            # cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s) RETURNING ID', (username, password, email,))
            connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg=msg)


@app.route('/exam')
def exam():
    pass


if __name__ == '__main__':
    app.run()
