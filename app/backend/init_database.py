from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Make sure to import the text function
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from constants import DB_PATH

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_PATH
app.config["SQLALCHEMY:TRACK_MODIFICATIONS"] = False

print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Create an instance of the Migrate class and pass the Flask app and SQLAlchemy db object
migrate = Migrate(app, db)


    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    chat_histories = db.relationship("ChatHistory", backref="user", lazy=True)

    def __init__(self, username):
        self.username = username

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username")

user_schema = UserSchema()
user_schemas = UserSchema(many=True)

class ChatHistory(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    chat_name = db.Column(db.String(40), nullable=False)
    messages = db.Column(db.Text())

    def __init__(self, user_id, chat_name, messages):
        self.user_id = user_id
        self.chat_name = chat_name
        self.messages = messages

class ChatHistorySchema(ma.Schema):
    class Meta:
        fields = ("chat_id", "user_id", "chat_name", "messages")

chat_schema = ChatHistorySchema()
chat_schemas = ChatHistorySchema(many=True)


with app.app_context():
    # Obtain a database connection
    connection = db.engine.connect()

    try:

        # Create tables
        db.create_all()
        print("CREATED")

    finally:
        # Close the connection
        connection.close()

