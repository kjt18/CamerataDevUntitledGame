import bcrypt
from flask import Flask, render_template, session, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, emit, leave_room

app = Flask(__name__)
app.secret_key = 'one2three4five6'  # TODO: 'SECURITY RISK' :: we need to remove this portion of code before deployment
socketio = SocketIO(app)

# TODO: 'SECURITY RISK' :: we need to remove this portion of code before deployment
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

# list of active game lobbies
game_lobbies = []


def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


# Helper function for checking password hash
def check_password(password, hash_value):
    return bcrypt.checkpw(password.encode('utf-8'), hash_value)


# Define function to start a new instance

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# TODO: 'TESTING' :: we need to test for other possible user inputs that would break the register feature
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


# TODO: 'TESTING' :: we need to test for other possible user inputs that would break the logout feature
# logout goes here
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))


# TODO: 'TESTING' :: we need to test for other possible user inputs that would break the login feature
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
    session['userid'] = user["id"]
    return redirect(url_for('index'))


# game page defined here, displays active lobbies
@app.route('/game')
def game():
    username = session.get('username')
    if username is None:
        # redirect the user to the login page if they're not logged in
        return redirect(url_for('login'))
    return render_template('game.html')


@app.route('/lobby')
def lobby():
    username = session.get('username')
    if username is None:
        # redirect the user to the login page if they're not logged in
        return redirect(url_for('login'))
    return render_template('lobby.html')


@socketio.on('connect')
def handle_connect():
    # emit the list of game lobbies to the newly connected client
    emit('game_lobbies', game_lobbies)


@socketio.on('create_lobby')
def handle_create_lobby(data):
    # add the new lobby to the list of game lobbies
    game_lobbies.append({'name': data['name'], 'users': [session['username']]})
    # emit the updated list of game lobbies to all connected clients
    emit('game_lobbies', game_lobbies, broadcast=True)


@socketio.on('join_lobby')
def handle_join_lobby(data):
    # find the game lobby by name and add the user to it
    for lobby in game_lobbies:
        if lobby['name'] == data['name']:
            lobby['users'].append(session['username'])
    # emit the updated list of game lobbies to all connected clients
    emit('game_lobbies', game_lobbies, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    username = session['username']
    # remove the user from any game lobbies they were in
    for lobby in game_lobbies:
        if username in lobby['users']:
            lobby['users'].remove(username)
            emit('user_left_lobby', {'username': username}, room=lobby['name'])
    # emit the updated list of game lobbies to all connected clients
    emit('game_lobbies', game_lobbies, broadcast=True)


# currently unused, saving public route for future use
@app.route('/public')
def public():
    return render_template('public.html')


# currently unused, saving private route for future use
@app.route('/private')
def private():
    return render_template('private.html')


# about page route defined here
@app.route('/about')
def about():
    return render_template('about.html')


# saved for testing purposes
# if __name__ == '__main__':
#     app.run(debug=True)

# Start the app
# save for now, pycharm UI doesn't like this very much.
# if __name__ == '__main__':
#     socketio.run(app, host="127.0.0.1", port=5000, debug=True)

if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=5000)
