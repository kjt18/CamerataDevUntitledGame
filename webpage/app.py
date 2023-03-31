import bcrypt
import uuid
from flask import Flask, render_template, session, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, emit, join_room, leave_room

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
    session_id = session.get('id')
    if session_id is not None:
        # Remove session from sessions table
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM sessions WHERE id = %s', (session_id,))
        mysql.connection.commit()
        cur.close()

        # Remove user session from user_sessions table
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM user_sessions WHERE session_id = %s', (session_id,))
        mysql.connection.commit()
        cur.close()

    session.clear()
    return redirect(url_for('index'))


# TODO: 'TESTING' :: we need to test for other possible user inputs that would break the login feature
# login goes here
@socketio.on('connect')
def on_connect():
    print('Connected to server')


@socketio.on('login')
def on_login(data):
    username = data['username']

    # Check if username exists in the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM accounts WHERE username = %s', (username,))
    user = cur.fetchone()

    if user is None:
        # Add error message and emit login_failed event
        error = 'Username does not exist'
        emit('login_failed', {'error': error})
    else:
        # Verify password
        hashed_password = user['phash'].encode('utf-8')
        if check_password(data['password'], hashed_password):
            # Create new session
            session_id = uuid.uuid4().hex
            session['id'] = session_id

            # Add session to sessions table
            cur.execute('INSERT INTO sessions (id) VALUES (%s)', (session_id,))
            mysql.connection.commit()

            # Add user session to user_sessions table
            cur.execute('INSERT INTO user_sessions (user_id, session_id) VALUES (%s, %s)', (user['id'], session_id))
            mysql.connection.commit()

            # Emit login_successful event only to the current client
            request.namespace.emit('login_successful', {'username': username})
        else:
            # Add error message and emit login_failed event
            error = 'Incorrect password'
            emit('login_failed', {'error': error})

    cur.close()


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

    # Redirect the user to the homepage after login
    return redirect(url_for('index'))


# game page defined here, displays active lobbies
@app.route('/game')
def game():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM lobby')
    lobbies = cur.fetchall()
    cur.close()
    return render_template('game.html', lobbies=lobbies)


# lobby page, currently only displays created lobbies
# @app.route('/lobby')
# def lobby():


@app.route('/create_lobby', methods=['GET', 'POST'])
def create_lobby():
    if request.method == 'POST':
        lobby_name = request.form['lobby_name']
        owner_name = request.form['owner_name']
        game_type = request.form['game_type']
        num_players = request.form['num_players']

        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO lobby (lobby_name, owner_name, game_type, num_players) VALUES (%s, %s, %s, %s)',
            (lobby_name, owner_name, game_type, num_players))
        mysql.connection.commit()
        cur.close()

        # join the lobby and emit a message to notify other users
        username = owner_name
        session['username'] = username
        join_room(lobby_name)

        # set the sid value in the session
        session['sid'] = request.sid

        # retrieve the sid value from the session
        sid = session.get('sid')
        if sid:
            emit('user_join', {'lobby_id': lobby_name, 'username': username, 'sid': sid}, broadcast=True)
        else:
            # handle the case where 'sid' value is not present in the session
            # for example, redirect to an error page or log the error
            pass

        # join the newly created lobby
        join_room(lobby_name)

        return redirect(url_for('lobby', lobby_id=lobby_name))

    return render_template('create_lobby.html')


@app.route('/join_lobby/<lobby_id>', methods=['GET', 'POST'])
def join_lobby(lobby_id):
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        join_room(lobby_id)
        emit('user_join', {'lobby_id': lobby_id, 'username': username, 'sid': request.sid}, room=lobby_id,
             include_self=False)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO lobby_players (lobby_id, username) VALUES (%s, %s)', (lobby_id, username))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('lobby'))

    return render_template('join_lobby.html', lobby_id=lobby_id)


@socketio.on('join')
def handle_join(data):
    lobby_id = data['lobby_id']
    username = data['username']
    sid = data['sid']  # get the sid value from the data parameter
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO lobby_players (lobby_id, username) VALUES (%s, %s)', (lobby_id, username))
    mysql.connection.commit()
    cur.close()
    emit('user_join', {'lobby_id': lobby_id, 'username': username, 'sid': sid}, room=lobby_id,
         include_self=False)  # send the message to the room and exclude the sender
    emit('user_join_notification', {'username': username}, room=lobby_id,
         include_self=False)  # send a notification message to other users in the room


@socketio.on('join')
def on_join(data):
    username = data['username']
    session['username'] = username
    join_room('lobby')
    emit('joined', {'username': username}, broadcast=True)


# handler for when user leaves lobby
@socketio.on('leave')
def handle_leave(data):
    lobby_id = data['lobby_id']
    username = data['username']
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM lobby_players WHERE lobby_id = %s AND username = %s', (lobby_id, username))
    mysql.connection.commit()
    cur.close()
    emit('user_leave', {'lobby_id': lobby_id, 'username': username}, broadcast=True)


# TODO: need to figure out how to get into specific lobby to join/leave
# @app.route('/leave_lobby/<int:lobby_id>', methods=['POST'])
# def leave_lobby(lobby_id):
#     username = request.form['username']
#     cur = mysql.connection.cursor()
#     cur.execute('DELETE FROM lobby_players WHERE lobby_id = %s AND username = %s', (lobby_id, username))
#     mysql.connection.commit()
#     cur.close()
#     return redirect(url_for('lobby'))


# handles user interaction when user leaves lobby
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    session.pop('username', None)
    leave_room('lobby')
    emit('left', {'username': username}, broadcast=True)


# handles messages being sent and displayed
@socketio.on('message')
def handle_message(data):
    username = session['username']
    message = data['message']
    emit('message', {'username': username, 'message': message}, room='lobby')


@socketio.on('disconnect')
def on_disconnect():
    print('Disconnected from server')


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
