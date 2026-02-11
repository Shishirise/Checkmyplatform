import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

# ---------- ROUTES ----------
@app.route("/")
def home():
    return "✅ CheckMyPlatform backend will be LIVE SOON"

@app.route("/player")
def player():
    return render_template("player.html")

@app.route("/agent")
def agent():
    return render_template("agent.html")

# ---------- SOCKET EVENTS ----------
@socketio.on("connect")
def connect():
    print("Client connected")

@socketio.on("join")
def join(data):
    room = data["room"]   # room = player_id
    join_room(room)
    print(f"Joined room: {room}")

@socketio.on("send_message")
def send_message(data):
    emit(
        "receive_message",
        {
            "sender": data["sender"],   # "player" or "agent"
            "message": data["message"]
        },
        room=data["room"]
    )

@socketio.on("disconnect")
def disconnect():
    print("Client disconnected")

# ---------- START ----------
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
