import jsonpickle.ext.numpy as jsonpickle_numpy
import os
from flask import Flask, jsonify, request, session

import jsonpickle


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
from modelpy_abm.main import AgentModel

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

    username, repo, repoData, model_parameters = (
        data["username"],
        data["repo"],
        data["repoData"],
        data["parameters"],
    )

    if repoData:
        return jsonify(getGitHub(username, repo, repoData))
    else:
        github_url = (
            f"https://raw.githubusercontent.com/{username}/{repo}/main/model.py"
        )

        response = requests.get(github_url)
        code = response.text

    print(code)
    exec(code)
    model = eval("constructModel()")
    params = attribs(model)

    if model_parameters:
        for param in model_parameters:
            try:
                model_parameters[param] = float(model_parameters[param])
            except:
                print(f"Failed to convert {param}")
                continue
        print(model_parameters)
        model.update_parameters(model_parameters)
        model["num_nodes"] = int(model["num_nodes"])
    model_parameters = {
        parameter: model[parameter] for parameter in model.list_parameters()
    }
    model.initialize_graph()
    graph = model.get_graph()
    nodes, edges = [node for node in graph.nodes(data=True)], [
        edge for edge in graph.edges(data=True)
    ]

    graphData = {
        "nodeData": nodes,
        "edgeData": edges,
        "classParams": model.list_parameters(),
        "parameters": model_parameters,
    }
    session["model"] = jsonpickle.encode(model)
    session["parameters"] = model.list_parameters()
    session["code"] = code
    return graphData


# {timesteps: int} -> graphData: {nodeData, edgeData, meanVals}
@app.post("/timestep")
def timestep_response():
    data = request.get_json()
    if session.get("model") and session.get("code"):
        try:
            timesteps = data["timesteps"]
        except:
            return data
        else:
            code = session["code"]
            exec(code)
            model = jsonpickle.decode(session["model"])
            data = timestep(model.get_graph(), model, timesteps)
        return data
    print("Couldn't find model")
    return data
