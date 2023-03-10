# from flask import Flask, render_template

from flask import Flask, render_template, request
from flask_mysqldb import MySQL

# import os

# DOG_FOLDER = os.path.join('static', 'dog_photo')

app = Flask(__name__)

# app.config['UPLOAD_FOLDER'] = DOG_FOLDER

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)


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

    if request.method == 'POST':
        name = request.form['username']
        age = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''', (name, age))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"


if __name__ == '__main__':
    app.run(debug=True)
