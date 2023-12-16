from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Make sure to import the text function
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate

pip install mysqlclient

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:gamefan2714@localhost/test_llm_app"
app.config["SQLALCHEMY:TRACK_MODIFICATIONS"] = False

print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Create an instance of the Migrate class and pass the Flask app and SQLAlchemy db object
migrate = Migrate(app, db)


# class Articles(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     titles = db.Column(db.String(100))
#     body = db.Column(db.Text())
    
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


# with app.app_context():
#     # Obtain a database connection
#     connection = db.engine.connect()

#     try:
#         # Perform a simple query to check the connection
#         # result1 = connection.execute(text("USE test_llm_app"))
#         result2 = connection.execute(text("SHOW TABLES"))

#         # row = result1.fetchone()
#         row2 = result2.fetchall()
#         print("blub:", row2)
#         # print("bib:", row)

#         # Create tables
#         db.create_all()
#         print("CREATED")

#     finally:
#         # Close the connection
#         connection.close()


#############################################################################
#############################################################################
########################## User CRUD Operations #############################
#############################################################################
#############################################################################
@app.route("/get_users", methods=["GET"])
def get_user():
    try:
        # Use Flask-SQLAlchemy with explicit text for the query
        all_user = User.query.all()
        results = user_schemas.dump(all_user)
        return jsonify(results)
    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({'error': str(e)}), 500


@app.route("/get_user/<id>", methods=["GET"])
def user_details(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)



@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    username = data.get("username")

    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    # If the username doesn't exist, add the new user
    new_user = User(username=username)

    try:
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)
    except Exception as e:
        # Handle exceptions, such as database errors
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/rename/<id>", methods=["PUT"])
def rename_user(id):
    user = db.session.get(User, id)

    # Ensure the user exists before updating
    if user is None:
        return jsonify({"message": "User not found"}), 404

    username = request.get_json().get("username")
    user.username = username

    db.session.commit()

    return user_schema.jsonify(user)

@app.route("/delete/<id>", methods=["DELETE"])
def delete_user(id):
    user = db.session.get(User, id)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


#############################################################################
#############################################################################
########################## Chat CRUD Operations #############################
#############################################################################
#############################################################################

@app.route("/user_chats/<id>", methods=["GET"])
def user_chats(id):
    user = User.query.get(id)
    chat = ChatHistory.query.filter_by(user_id=id).all()
    return chat_schemas.jsonify(chat)

@app.route("/get_chats", methods=["GET"])
def get_chats():
    try:
        # Use Flask-SQLAlchemy with explicit text for the query
        all_chats = ChatHistory.query.all()
        results = chat_schemas.dump(all_chats)
        return jsonify(results)
    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({'error': str(e)}), 500

@app.route("/add_chat", methods=["POST"])
def add_chat():
    data = request.get_json()

    user_id = data.get("user_id")
    chat_name = data.get("chat_name")
    messages = data.get("messages")

    # Create a new ChatHistory instance
    new_chat = ChatHistory(user_id=user_id, chat_name=chat_name, messages=messages)

    # Add the new_chat to the database
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({"message": "Chat added successfully"})




if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)