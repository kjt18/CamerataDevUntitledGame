from flask import Flask, render_template
# import os

# DOG_FOLDER = os.path.join('static', 'dog_photo')

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = DOG_FOLDER


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


if __name__ == '__main__':
    app.run(debug=True)
