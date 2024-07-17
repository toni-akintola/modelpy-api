import jsonpickle.ext.numpy as jsonpickle_numpy
import os
from flask import Flask, jsonify, request, session

import jsonpickle
from typing import Literal
import random

from redis import Redis
import networkx as nx
import random

import numpy as np
import statistics
import ast
import requests
from flask_session import Session
from flask_cors import CORS

from models.models import attribs, getGitHub, timestep

app = Flask(__name__)
app.config.from_object(__name__)

app.config["SECRET_KEY"] = os.urandom(12)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True  # Secure since it's in production
# 'None' for cross-domain requests
app.config["SESSION_COOKIE_SAMESITE"] = "None"


# SESSION_REDIS = Redis(host="localhost", port=6379)

Session(app)
CORS(app, supports_credentials=True)
jsonpickle_numpy.register_handlers()


@app.route("/")
def hello_world():
    return "Hello, World!"


# {username: str, repo: str, repoData: bool} -> <- graphData: {nodeData, edgeData, classParams}
@app.post("/initialize")
def initialize_response():
    data = request.get_json()

    username, repo, repoData, code = (
        data["username"],
        data["repo"],
        data["repoData"],
        data["code"],
    )

    if repoData:
        return jsonify(getGitHub(username, repo, repoData))

    p = ast.parse(code)
    className = None
    classParams = []
    for node in ast.walk(p):
        if isinstance(node, ast.ClassDef):
            className = node.name
            break

    add_on_code = f"""new_model = {className}()"""
    code = code + add_on_code
    print(code)
    exec(code)
    model = eval("new_model")
    params = attribs(model)
    classParams = {param: getattr(model, param) for param in params}
    model.initialize_graph()
    graph = model.graph
    nodes, edges = [node for node in graph.nodes(data=True)], [
        edge for edge in graph.edges(data=True)
    ]
    print(nodes, edges)
    graphData = {"nodeData": nodes,
                 "edgeData": edges, "classParams": classParams}
    session["model"] = jsonpickle.encode(model)
    session["code"] = code
    session["className"] = className
    return graphData


# {timesteps: int} -> graphData: {nodeData, edgeData, meanVals}
@app.post("/timestep")
def timestep_response():
    data = request.get_json()
    if session.get("model") and session.get("code") and session.get("className"):
        try:
            timesteps = data["timesteps"]
        except:
            return data
        else:
            code = session["code"]
            className = session["className"]
            exec(code)
            cls = eval(className)
            model = jsonpickle.decode(session["model"], classes=cls)
            data = timestep(model.graph, model, timesteps)
        return data
    return data
