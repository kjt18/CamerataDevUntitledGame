from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
import bcrypt

from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.secret_key = 'one2three4five6'  # we need to remove this portion of code before deployment, 'security risk'
socketio = SocketIO(app)

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

# Define lobby dictionary to keep track of users and their groups
groups = {}


# Define helper function to get the group number of a user
def get_group(username):
    for group in groups:
        if username in groups[group]:
            return group
    return None


def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


# Helper function for checking password hash
def check_password(password, hash_value):
    return bcrypt.checkpw(password.encode('utf-8'), hash_value)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# register now goes here
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']
    password = request.form['password']
    session['username'] = username
    hashed_password = encrypt_password(password)

    # Check if username already exists in the database
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()

    if user is not None:
        # Username already exists, add error message and render register page again
        error = 'Username already exists'
        return render_template('register.html', error=error)

    # Create new account
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO accounts (username, phash) VALUES (%s, %s)",
                   (username, hashed_password.decode('utf-8')))
    mysql.connection.commit()
    cursor.close()

    return render_template('index.html')


# logout goes here
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))


# login goes here
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
    hashed_password = user['phash'].encode('utf-8')
    if not check_password(password, hashed_password):
        # Add error message and render login page again
        error = 'Incorrect password'
        return render_template('login.html', error=error)

    # Set session username and redirect to index
    session['username'] = username
    return redirect(url_for('index'))


# lobby goes here
@app.route('/lobby')
def lobby():
    # Check if user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    # Get user's group or create a new group if user is not in any group
    username = session['username']
    group = get_group(username)
    if group is None:
        group = len(groups) + 1
        groups[group] = [username]

    # Render lobby page with group number and list of users in the same group
    return render_template('lobby.html', group=group, users=groups[group])


# Define SocketIO event handlers
@socketio.on('join')
def join(data):
    # Join a SocketIO room corresponding to the user's group
    username = session['username']
    group = get_group(username)
    join_room(group)
    emit('joined', {'username': username}, room=group)


@socketio.on('leave')
def leave(data):
    # Leave the SocketIO room corresponding to the user's group
    username = session['username']
    group = get_group(username)
    leave_room(group)
    emit('left', {'username': username}, room=group)

# about page route defined here
@app.route('/about')
def about():
    return render_template('about.html')

# game page defined here
@app.route('/game')
def game():
    return render_template('game.html')

# currently unused, saving public route for future use
@app.route('/public')
def public():
    return render_template('public.html')

# currently unused, saving private route for future use
@app.route('/private')
def private():
    return render_template('private.html')

# saved for testing purposes
# if __name__ == '__main__':
#     app.run(debug=True)

# Start the app
if __name__ == '__main__':
    socketio.run(app)
