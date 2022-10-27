from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/zahraa.emara/Desktop/rest_api_using_python_and_flask/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
