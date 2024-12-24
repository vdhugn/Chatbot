from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from chat_gemini import chat

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

# Handle messages from the frontend
@socketio.on("send_message")
def handle_message(data):
    query = data.get("message", "")
    if not query:
        emit("receive_message", {"error": "No query provided"})
        return

    # Call the chat function and get a response
    try:
        response = chat(query=query, topk=10)  # Pass user query to the chatbot
        emit("receive_message", {"message": response, "from": "chatbot"})
    except Exception as e:
        emit("receive_message", {"error": str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True)
