def db_config(app):

    app.secret_key = 'one2three4five6'

    app.config['MYSQL_USER'] = 'capstonesa'
    app.config['MYSQL_PASSWORD'] = 'C@pstonepassword'
    app.config['MYSQL_DB'] = 'capstone'
    app.config['MYSQL_HOST'] = 'capstone-server.mysql.database.azure.com'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    # added to use https
    # app.config['SERVER_NAME'] = 'yourdomain.com'  # replace with your domain name
    app.config['PREFERRED_URL_SCHEME'] = 'https'

    return app
