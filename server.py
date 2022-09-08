from flask import Flask, request
from flask_cors import CORS
from os import getenv, kill, getpid
from signal import signal, SIGTERM, SIGINT
from two_factor_code import on_code_received
from threading import Thread
from time import sleep

app = Flask(__name__, static_folder="html")

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

@app.route("/kill", methods=["POST"])
def kill_server():
    print("[INFO] Waiting to stop server {}".format(getpid()))
    kill(getpid(), SIGINT)

    return {
        "stopping": True
    }


def start_http_server():
    CORS(app, resources=r"/*")
    app.run(getenv("SERVER_IP"), port=3333, debug=False)
