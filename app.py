import os
from flask import Flask, jsonify, request, session

# import jsonpickle
from typing import Literal
import random

# from flask_cors import CORS
# from redis import Redis
# import networkx as nx
import random

# import numpy as np
# import statistics
# import ast
# import requests
from flask_session import Session

app = Flask(__name__)
app.config.from_object(__name__)

app.config["SECRET_KEY"] = os.urandom(12)
app.config["SESSION_TYPE"] = "filesystem"

# SESSION_REDIS = Redis(host="localhost", port=6379)

Session(app)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/set")
def set():
    session["key"] = random.randint(0, 100)

    return str(session["key"])


@app.route("/get")
def get():
    if session.get("key"):
        return str(session["key"])
    return ""
