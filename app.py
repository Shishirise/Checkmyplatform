from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/player")
def player():
    return render_template("player.html")

@app.route("/agent")
def agent():
    return render_template("agent.html")

if __name__ == "__main__":
    app.run()
