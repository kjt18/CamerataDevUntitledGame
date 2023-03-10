from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL

import bcrypt

app = Flask(__name__)
app.secret_key = 'one2three4five6'

# Configure MySQL database
app.config['MYSQL_USER'] = 'capstonesa'
app.config['MYSQL_PASSWORD'] = 'C@pstonepassword'
app.config['MYSQL_DB'] = 'capstone'
app.config['MYSQL_HOST'] = 'capstone-server.mysql.database.azure.com'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# added to use https
# app.config['SERVER_NAME'] = 'yourdomain.com'  # replace with your domain name
app.config['PREFERRED_URL_SCHEME'] = 'https'
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


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']
    password = request.form['password']
    session['username'] = username
    hashed_password = encrypt_password(password)

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO accounts (username, phash) VALUES (%s, %s)", (username, hashed_password))
    mysql.connection.commit()
    cursor.close()

    return render_template('index.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    # Check if username exists in the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM accounts WHERE username = %s', (username,))
    user = cur.fetchone()
    cur.close()

    if user is None:
        # Add error message and render login page again
        error = 'Username does not exist'
        return render_template('login.html', error=error)

    # Verify password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), user['password'].encode('utf-8'))
    if hashed_password != user['password'].encode('utf-8'):
        # Add error message and render login page again
        error = 'Incorrect password'
        return render_template('login.html', error=error)

    # Set session username and redirect to index
    session['username'] = username
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
