from flask import Flask, request
from flask_cors import CORS
from os import getenv
from two_factor_code import on_code_received
from threading import Thread

app = Flask(__name__, static_folder="html")
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", methods=["GET"])
def handle():
    return app.send_static_file("index.html")

@app.route("/code", methods=["POST"])
def show_code():
    print("[INFO] POST on /code endpoint")
    code_received = request.data.decode()
    on_code_received(code_received)

    return {
        "code_received": code_received
    }

def start_http_server():
    t = Thread(target=app.run(getenv("SERVER_IP"), port=3333, debug=False))
    t.start()
    
