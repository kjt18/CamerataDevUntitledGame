from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)
api = Api(app)

# Define the necessary routes and endpoints
api.add_resource(Login, '/login')
api.add_resource(Files, '/files')
api.add_resource(File, '/files/<file_id>')
api.add_resource(Preview, '/preview/<file_id>')
api.add_resource(Preferences, '/preferences')

if __name__ == '__main__':
    app.run(debug=True)
