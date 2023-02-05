import hashlib
import mysql.connector


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_account():
    cnx = mysql.connector.connect(user='capAdmin', password='capAdmin',
                                  host='BorelliSQL',
                                  database='capstone')
    cursor = cnx.cursor()

    username = input("Enter a username: ")

    query = "SELECT count(id) FROM accounts WHERE username = %s;"

    # check if username already exists
    cursor.execute(query, (username,))
    for count in cursor:

        if 0 not in count:
            print("Username already exists. Please try again.")
            cursor.close()
            cnx.close()
            return 0

    password = input("Enter a password: ")
    password = hash_password(password)

    query = ("INSERT INTO accounts(username, phash) "
             "values(%s, %s);")
    cursor.execute(query, (username, password))
    cnx.commit()

    print("Account created successfully!")

    username = ''
    password = ''

    cursor.close()
    cnx.close()

    return 1


def login():
    cnx = mysql.connector.connect(user='capAdmin', password='capAdmin',
                                  host='BorelliSQL',
                                  database='capstone')
    cursor = cnx.cursor()

    username = input("Enter your username: ")
    password = input("Enter your password: ")
    password = hash_password(password)

    query = "SELECT count(id) FROM accounts WHERE username = %s AND phash = %s;"

    cursor.execute(query, (username, password))
    for count in cursor:

        if 0 not in count:
            print("Login successful!")

            cursor.close()
            cnx.close()

            return 0

        print("Incorrect username or password. Please try again.")

        cursor.close()
        cnx.close()

        return 1


if __name__ == '__main__':
    answer = input("Enter '1' to create a new account or '2' to login to an existing account: ")
    if answer == '1':
        w = 0
        while w == 0:
            w = create_account()
    elif answer == '2':
        w = 1
        while w == 1:
            w = login()
