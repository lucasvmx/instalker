from flask import Flask, request
from flask_cors import CORS
from os import getenv, kill, getpid
from signal import SIGINT
from two_factor_code import on_code_received
from logging import info

app = Flask(__name__, static_folder="html")

@app.route("/", methods=["GET"])
def handle():
    return app.send_static_file("index.html")

@app.route("/code", methods=["POST"])
def show_code():
    info("received POST on /code")
    code_received = request.data.decode()
    on_code_received(code_received)

    return {
        "code_received": code_received
    }

@app.route("/kill", methods=["POST"])
def kill_server():
    info("waiting to stop server {}".format(getpid()))
    kill(getpid(), SIGINT)

    return {
        "stopping": True
    }


def start_http_server():
    CORS(app, resources=r"/*")
    app.run(getenv("SERVER_IP"), port=3333, debug=False)
