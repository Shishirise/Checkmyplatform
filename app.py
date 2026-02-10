import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

@socketio.on("connect")
def connect():
    print("✅ Client connected")

@socketio.on("join")
def join(data):
    room = data["room"]
    join_room(room)
    print(f"📥 Joined room: {room}")

@socketio.on("join_seller")
def join_seller():
    join_room("sellers")
    print("🧑‍💼 Seller joined sellers room")

@socketio.on("send_message")
def send_message(data):
    print("📨 Message received:", data)

    # Send to buyer room
    emit(
        "receive_message",
        {
            "sender": data["sender"],
            "message": data["message"]
        },
        room=data["room"]
    )

    # Send to seller inbox
    emit(
        "receive_message",
        {
            "sender": data["sender"],
            "message": data["message"]
        },
        room="sellers"
    )

@socketio.on("disconnect")
def disconnect():
    print("❌ Client disconnected")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
