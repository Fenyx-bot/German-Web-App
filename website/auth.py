from datetime import datetime
from flask import Blueprint, render_template, request, flash
import pymysql

auth = Blueprint('auth', __name__)

hostname = 'localhost'
dbUser = 'root'
dbPassword = ''

userData = None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')


        db = pymysql.connections.Connection(
            database='pythontest',
            host=hostname,
            user=dbUser,
            password=dbPassword,
        )
        

        cursor = db.cursor()
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))

        data = cursor.fetchone()

        cursor.close() 
        db.close()

        if data != None:
            userData = data
            flash('Logged in successfully!', category='success')
            return render_template("home.html", username=username, email=data[1], password=password)
        else:
            flash('Username or password is incorrect.', category='error')
    return render_template("login.html")


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Please make sure that your email is correct.', category='error')

        elif len(username) < 2:
            flash('Username must be greater than 2 characters.', category='error')

        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')

        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')

        else:
            print(email, username, password1)

            db = pymysql.connections.Connection(
                database='pythontest',
                host=hostname,
                user=dbUser,
                password=dbPassword,
            )
            
            used = False

            cursor = db.cursor()
            cursor.execute('SELECT * FROM user')
            for row in cursor:
                if row[0] == username:
                    flash('Username already exists.', category='error')
                    used = True
                    break
                if row[1] == email:
                    flash('Email already exists.', category='error')
                    used = True
                    break
            if not used:
                cursor.execute('INSERT INTO user (username, email, password) VALUES (%s, %s, %s)', (username, email, password1))
                cursor.connection.commit()
                flash('Account created!', category='success')
                return render_template("home.html", username=username, email=email, password=password1)
            cursor.close()
            db.close()

    return render_template("sign_up.html")


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"