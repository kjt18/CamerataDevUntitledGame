from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL

import bcrypt

# import os

# DOG_FOLDER = os.path.join('static', 'dog_photo')

app = Flask(__name__)

# app.config['UPLOAD_FOLDER'] = DOG_FOLDER

# localhost
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'flask'
# mysql = MySQL(app)

# Configure MySQL database
app.config['MYSQL_USER'] = 'capstonesa'
app.config['MYSQL_PASSWORD'] = 'C@pstonepassword'
app.config['MYSQL_DB'] = 'capstone'
app.config['MYSQL_HOST'] = 'capstone-server.mysql.database.azure.com'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


# Helper function for checking password hash

def check_password(password, hash_value):
    return bcrypt.checkpw(password.encode('utf-8'), hash_value.encode('utf-8'))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# @app.route('/')
# @app.route('/index')
# def show_index():
#     full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'dog.png', 'dog2.png', 'dog3.png')
#     return render_template("index.html", user_image=full_filename)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/game')
def game():
    return render_template('game.html')


@app.route('/public')
def public():
    return render_template('public.html')


@app.route('/private')
def private():
    return render_template('private.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    hashed_password = encrypt_password(password)

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO accounts (username, phash) VALUES (%s, %s)", (username, hashed_password))
    mysql.connection.commit()
    cursor.close()

    # url = url_for('index', _external=True, _scheme='https')
    return render_template('game.html')


if __name__ == '__main__':
    app.run(debug=True)
