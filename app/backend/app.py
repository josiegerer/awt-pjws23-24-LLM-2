from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Make sure to import the text function
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from llm_service import MessageProcessor, EvalProcessor, EndlessProcessor

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
    # user = User.query.get(id)
    user = db.session.get(User, id)
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

@app.route("/add_message/<chat_id>", methods=["POST"])
def add_message(chat_id):
    chat = ChatHistory.query.get(chat_id)

    if chat is None:
        return jsonify({"message": "Chat not found"}), 404

    new_message = request.get_json().get("message")

    if new_message is not None:
        chat.messages += "\\n" + new_message  # Assuming messages are newline-separated
        db.session.commit()

        return jsonify({"message": "Message added successfully"})
    else:
        return jsonify({"message": "Invalid message"}), 400

@app.route("/process_message/<int:chat_id>", methods=["POST"])
def process_message(chat_id):
    try:
        # Get the message from the request
        data = request.get_json()
        user_message = data.get("message")
        grammar_assistant = data.get("grammar", False)  # Default to False if the parameter is not present
        informal_assistant = data.get("informal", False)  # Default to False if the parameter is not present
        print(data)
        print(user_message)
        print(grammar_assistant)
        if grammar_assistant:
            # Process message for grammar assistance
            chat_type = "grammar"
        else:
            # Process message for normal conversation
            chat_type = "conversation"
        
        if informal_assistant:
            # Process message for informal conversation
            formality = "informal"
        else:
            # Process message for normal conversation
            formality = "formal"            

        # Update the chat messages in the database
        # You need to modify this based on your database model
        chat = ChatHistory.query.get(chat_id)

        # Process the user message using the MessageProcessor class
        processor = MessageProcessor()
        processed_message = processor.process_message(user_message, chat_type, formality, chat.messages)
        chat.messages += "\\n" + user_message + "\\n" + processed_message  # Append the processed message
        db.session.commit()

        return jsonify({"success": True, "message": processed_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze_conversation/<int:chat_id>", methods=["POST"])
def analyze_conversation(chat_id):
    try:
        # Get the message from the request
        data = request.get_json()
        grammar_assistant = data.get("grammar", False)  # Default to False if the parameter is not present
        informal_assistant = data.get("informal", False)  # Default to False if the parameter is not present
        if grammar_assistant:
            # Process message for grammar assistance
            chat_type = "grammar"
        else:
            # Process message for normal conversation
            chat_type = "conversation"
        
        if informal_assistant:
            # Process message for informal conversation
            formality = "informal"
        else:
            # Process message for normal conversation
            formality = "formal"            

        chat = ChatHistory.query.get(chat_id)

        processor = EvalProcessor()
        processed_message = processor.eval_conversation(chat_type, formality, chat.messages)
        print("#"*50)
        print(processed_message)
        chat.messages += "\\n" + "Your current conversation gets analyzed and evaluated" + "\\n" + processed_message  # Append the processed message
        db.session.commit()

        return jsonify({"success": True, "message": processed_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/self_conversation/<int:chat_id>", methods=["POST"])
def self_conversation(chat_id):
    try:
        data = request.get_json()
        print(data)
        user_message = data.get("message")
        topic = data.get("topic")
        print(topic)
        print(user_message)
        informal_assistant = data.get("informal", False)        
        print(informal_assistant)
        if informal_assistant:
            formality = "informal"
        else:
            formality = "formal"

        chat = ChatHistory.query.get(chat_id)

        processor = EndlessProcessor(topic=topic)
        processed_message = processor.process_message(formality, chat.messages, user_message)        

        print("#"*50)
        print(processed_message)
        chat.messages += "\\n" + processed_message  # Append the processed message
        db.session.commit()

        return jsonify({"success": True, "message": processed_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)