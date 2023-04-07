import re

import bcrypt
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, emit

import game_handler

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

# GameHnadler object
gh = game_handler.GameHandler()


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

    # Check if username already exists in the database
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()

    if user is not None:
        # Username already exists, add error message and render register page again
        error = 'Username already exists'
        return render_template('register.html', error=error)

    while True:
        if not re.search("[A-Z]", password):
            error = 'Password must be between 6 to 20 characters, ' \
                    'and contain at least one capital letter and number or symbol'
            return render_template('register.html', error=error)
        elif not re.search("[0-9\W]", password):
            error = 'Password must be between 6 to 20 characters, ' \
                    'and contain at least one capital letter and number or symbol'
            return render_template('register.html', error=error)
        elif len(password) < 6 or len(password) > 20:
            error = 'Password must be between 6 to 20 characters, ' \
                    'and contain at least one capital letter and number or symbol'
            return render_template('register.html', error=error)
        else:
            break

    session['username'] = username
    hashed_password = encrypt_password(password)

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


# TODO: 'TESTING' :: we need to test for other possible user inputs that would break the page

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    # retrieve player stats
    cur = mysql.connection.cursor()
    cur.execute('select * From playerstatsview where id = %s', (session['userid'],))
    playerStats = cur.fetchall()
    cur.close()

    if playerStats is None:
        # Add error message and render login page again
        error = 'Player Stats do not exist'
        return render_template('index.html', error=error)

    p = "<tr><th>High Score</th><th>Highest Round</th><th>Won</th><th>Lost</th><th>Tied</th></tr>"

    for row in playerStats:
        p = p + "<tr\><td>%s</td>" % row['High Score']
        p = p + "<td>%s</td>" % row["Highest Round"]
        p = p + "<td>%s</td>" % row["Won"]
        p = p + "<td>%s</td>" % row["Lost"]
        p = p + "<td>%s</td></tr>" % row["Tied"]

    session['mtable'] = p

    # retrieve player history
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM matchhistoryview where id = %s LIMIT 10', (session['userid'],))
    playerHist = cur.fetchall()
    cur.close()

    if playerHist is None:
        # Add error message and render login page again
        error = 'Match History does not exist'
        return render_template('index.html', error=error)

    h = "<tr><th>Match Time</th><th>Player Name</th><th>Player Score</th>" \
        "<th>Opponent Name</th><th>Opponent Score</th><th>Round</th><th>Result</th></tr>"

    for row in playerHist:
        h = h + "<tr><td>%s</td>" % row["matchtime"]
        h = h + "<td>%s</td>" % row["Player Name"]
        h = h + "<td>%s</td>" % row["Player Score"]
        h = h + "<td>%s</td>" % row["Opponent Name"]
        h = h + "<td>%s</td>" % row["Opponent Score"]
        h = h + "<td>%s</td>" % row["Round"]
        h = h + "<td>%s</td></tr>" % row["Result"]

    session['htable'] = h

    return render_template('stats.html', stats_string=session['mtable'], hist_string=session['htable'])


# game page defined here, displays active lobbies
@app.route('/game')
def game():
    username = session.get('username')
    if username is None:
        # redirect the user to the login page if they're not logged in
        return redirect(url_for('login'))
    return render_template('game.html')


import uuid
import multiprocessing


def generate_match_id():
    return str(uuid.uuid4())


def start_instance(pipe):
    # start the game instance and use the pipe to communicate with it
    pass  # placeholder


def create_match():
    # create a unique match_id, and pass the necessary parameters to the new_match method
    match_id = generate_match_id()  # implement this function to generate a unique match_id
    player1 = session.get('username')
    # player2 = None  # the second player may be added later

    # create a new match
    gh.new_match(match_id, player1)

    # emit a socket event to start the game
    socketio.emit('start_game', {'match_id': match_id})

    return match_id, player1


@app.route('/lobby')
def lobby():
    username = session.get('username')
    if username is None:
        # redirect the user to the login page if they're not logged in
        return redirect(url_for('login'))

    # create a new match and get the match_id and player1
    match_id, player1 = create_match()

    parent_conn, child_conn = multiprocessing.Pipe()

    # start the game instance process
    instance_process = multiprocessing.Process(target=start_instance, args=(child_conn,))
    instance_process.start()

    # start the generator process to send commands to the game instance
    generator_process = multiprocessing.Process(target=generate, args=(parent_conn,))
    generator_process.start()

    return render_template('lobby.html', match_id=match_id)


def generate(pipe):
    while True:
        # receive a command from the parent process
        command = pipe.recv()

        # send the command to the game instance
        response = gh.send_command(command)

        # send the response back to the parent process
        pipe.send(response)


@socketio.on('command')
def handle_command(data):
    match_id = data['match_id']
    player = session['username']
    command = data['command']
    result = gh.command(match_id, player, command)
    send_update(match_id, result)


# define a function to send updates to the client
def send_update(match_id, update):
    socketio.emit('update', {'match_id': match_id, 'update': update})


# define a function to receive commands from the client

@app.route('/command', methods=['POST'])
def command():
    command = request.json['command']
    gh.parent_conn.send(command)
    game_state = gh.parent_conn.recv()
    response = {'gameState': game_state}
    return jsonify(response)


# @app.route('/end_match/<match_id>')
# def end_match(match_id):
#     if gh.end_match(match_id):
#         return 'Match ended successfully'
#     else:
#         return 'Match not found'
#
#
# @app.route('/command/<match_id>/<player>/<command>')
# def command(match_id, player, command):
#     result = gh.command(match_id, player, command)
#     if result is not None:
#         return result
#     else:
#         return 'Match not found'


@app.route('/create_new_lobby')
def create_new_lobby():
    username = session.get('username')
    if username is None:
        # redirect the user to the login page if they're not logged in
        return redirect(url_for('login'))
    return render_template('create_new_lobby.html')


# TODO: test method to see if variables are properly getting called.
@socketio.on('create_lobby')
def handle_create_lobby(data):
    # find the lobby with the given name
    lobby = next((lobby for lobby in game_lobbies if lobby['name'] == data['name']), None)
    if lobby is None:
        # create a new lobby with the given name and add the creator as the first player
        lobby = {'name': data['name'], 'users': [session['username']], 'max_players': 1}
        game_lobbies.append(lobby)
    else:
        # add the user to an existing lobby with the same name
        lobby['users'].append(session['username'])

    if len(lobby['users']) == lobby['max_players']:
        # if the lobby now has two players, create a new match and start the game
        match_id = generate_match_id()
        player1 = lobby['users']
        gh.new_match(match_id, player1)
        socketio.emit('start_game', {'match_id': match_id})

    # emit the updated list of game lobbies to all connected clients
    emit('game_lobbies', game_lobbies, broadcast=True)


# @socketio.on('create_lobby')
# def handle_create_lobby(data):
#     # add the new lobby to the list of game lobbies
#     game_lobbies.append({'name': data['name'], 'users': [session['username']], 'max_players': 2})
#     # emit the updated list of game lobbies to all connected clients
#     emit('game_lobbies', game_lobbies, broadcast=True)


@socketio.on('join_lobby')
def handle_join_lobby(data):
    # find the game lobby by name and add the user to it
    for lobby in game_lobbies:
        if lobby['name'] == data['name']:
            if len(lobby['users']) < lobby['max_players']:  # check if lobby is full
                lobby['users'].append(session['username'])
                # emit the updated list of game lobbies to all connected clients
                socketio.emit('game_lobbies', game_lobbies, broadcast=True)
            else:
                # emit a message to the client that the lobby is full
                socketio.emit('lobby_full', {'message': 'This lobby is full.'})
                return


@socketio.on('leave_lobby')
def handle_leave_lobby(data):
    # find the game lobby by name and remove the user from it
    for lobby in game_lobbies:
        if lobby['name'] == data['name']:
            lobby['users'].remove(session['username'])
            # emit the updated list of game lobbies to all connected clients
            socketio.emit('game_lobbies', game_lobbies, broadcast=True)
        break


@socketio.on('connect')
def handle_connect():
    # emit the list of game lobbies to the newly connected client
    socketio.emit('game_lobbies', game_lobbies)


@socketio.on('disconnect')
def handle_disconnect():
    username = session['username']
    # remove the user from any game lobbies they were in
    for lobby in game_lobbies:
        if username in lobby['users']:
            lobby['users'].remove(username)
            socketio.emit('user_left_lobby', {'username': username}, room=lobby['name'])
    # emit the updated list of game lobbies to all connected clients
    socketio.emit('game_lobbies', game_lobbies, broadcast=True)


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
# save for now, pycharm UI doesn't like this very much.
# if __name__ == '__main__':
#     socketio.run(app, host="127.0.0.1", port=5000, debug=True)

if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=5000)
