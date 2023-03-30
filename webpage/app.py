from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
import bcrypt


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

    return render_template('stats.html', stats_string = session['mtable'], hist_string = session['htable'])




# lobby goes here
# Define the method for getting users in a lobby
def get_users_in_lobby(lobbyid):
    cur = mysql.connection.cursor()
    cur.execute('SELECT username FROM lobby_members WHERE lobbyid = %s', (lobbyid,))
    users = [row[0] for row in cur.fetchall()]
    cur.close()
    return users


# Define the Flask route for the lobby page
@app.route('/lobby')
def lobby():
    # Check if user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    # Get user's lobbyid or create a new lobby if user is not in any lobby
    username = session['username']
    cur = mysql.connection.cursor()
    cur.execute('SELECT lobbyid FROM lobby WHERE owner = %s', (username,))
    row = cur.fetchone()
    if row is not None:
        lobbyid = row['lobbyid']
    else:
        # Insert a new row into the lobby table and get the auto-generated id
        cur.execute('INSERT INTO lobby (owner) VALUES (%s)', (username,))
        mysql.connection.commit()
        lobbyid = cur.lastrowid
    cur.close()

    # Get the list of users in the lobby
    users = get_users_in_lobby(lobbyid)

    # Render lobby page with lobbyid and list of users in the same lobby
    return render_template('lobby.html', lobbyid=lobbyid, users=users)


# Define SocketIO event handlers
@socketio.on('join')
def join(data):
    # Join a SocketIO room corresponding to the user's lobbyid
    username = session['username']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT lobbyid FROM lobby WHERE owner = %s', (username,))
    row = cursor.fetchone()
    if row is not None:
        lobbyid = row[0]
    else:
        # Create a new lobby if user is not in any lobby
        cursor.execute('INSERT INTO lobby (owner) VALUES (%s)', (username,))
        mysql.connection.commit()
        lobbyid = cursor.lastrowid
    cursor.close()

    join_room(lobbyid)
    emit('joined', {'username': username}, room=lobbyid)


@socketio.on('leave')
def leave(data):
    # Leave the SocketIO room corresponding to the user's lobbyid
    username = session['username']
    lobbyid = get_lobby(username)
    leave_room(lobbyid)
    emit('left', {'username': username}, room=lobbyid)
    return render_template('game.html')


def get_lobby(username):
    cur = mysql.connection.cursor()
    cur.execute('SELECT lobbyid FROM lobby WHERE owner = %s', (username,))
    lobbyid = cur.fetchone()
    cur.close()
    if lobbyid:
        return lobbyid[0]
    else:
        cur = mysql.connection.cursor()
        cur.execute('SELECT lobbyid FROM lobby_members WHERE username = %s', (username,))
        lobbyid = cur.fetchone()
        cur.close()
        if lobbyid:
            return lobbyid[0]
        else:
            return None


# about page route defined here
@app.route('/about')
def about():
    return render_template('about.html')


# game page defined here
@app.route('/game')
def game():
    lobbyid = session.get('lobbyid')
    cur = mysql.connection.cursor()
    # cur.execute('SELECT lobbyid, owner, game_type, num_players FROM lobby WHERE lobbyid = %s', (lobbyid,))
    # cur.execute('SELECT lobbyid, owner, num_players FROM lobby WHERE lobbyid = %s', (lobbyid,))
    cur.execute('SELECT lobbyid, owner FROM lobby WHERE lobbyid = %s', (lobbyid,))
    lobby = cur.fetchone()
    cur.close()
    return render_template('game.html', lobby=lobby)


# currently unused, saving public route for future use
@app.route('/public')
def public():
    return render_template('public.html')


# currently unused, saving private route for future use
@app.route('/private')
def private():
    return render_template('private.html')


# saved for testing purposes
if __name__ == '__main__':
    app.run(debug=True)

# Start the app
# save for now, pycharm UI doesn't like this very much.
# if __name__ == '__main__':
#     socketio.run(app, host="127.0.0.1", port=5000, debug=True)
# if __name__ == '__main__':
#     socketio.run(app, host="127.0.0.1", port=5000, debug=True)