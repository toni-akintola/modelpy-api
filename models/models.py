from typing import Literal
import json
import jsonpickle
import requests
import ast
import networkx as nx
import random
import numpy as np
import statistics
import inspect
from emergent.main import AgentModel

VisGraphType = Literal["bar", "line", "network"]


class Vis:
    def __init__(self, dataKey: str, type: str, title: str = None):
        self.dataKey = dataKey
        self.type = type
        self.title = title


class Model:
    def __init__(
        self, id: str, username: str, repo: str, categories: str, visualizations: Vis
    ):
        self.id = id
        self.username = username
        self.repo = repo
        self.categories = categories
        self.visualizations = visualizations


class AgentModel:
    def __init__(self) -> None:
        self.graph: nx.Graph = None

    def initialize_graph():
        pass


models: list[Model] = [
    Model(
        id="kekoawong-zollman-bandit",
        username="kekoawong",
        repo="zollman-bandit",
        categories=["bandit-model", "bayesian-agents", "abm"],
        visualizations=[
            Vis(
                title="Nodes colored by their expectation for B",
                dataKey="b_expectation",
                type="network",
            ),
            Vis(
                title="Node expectations for B",
                dataKey="b_expectation",
                type="bar",
            ),
            Vis(
                title="Nodes colored by their expectation for A",
                dataKey="a_expectation",
                type="network",
            ),
            Vis(
                title="Node expectations for A",
                dataKey="a_expectation",
                type="bar",
            ),
            Vis(
                title="Node expectations for B over time",
                dataKey="b_expectation",
                type="line",
            ),
            Vis(
                title="Node expectations for A over time",
                dataKey="a_expectation",
                type="line",
            ),
        ],
    ),
    Model(
        id="kekoawong-wu-epistemic-advantage",
        username="kekoawong",
        repo="wu-epistemic-advantage",
        categories=["bandit-model", "bayesian-agents", "abm"],
        visualizations=[
            Vis(title="Nodes colored by type", dataKey="type", type="network"),
            Vis(
                title="Nodes colored by learned belief",
                dataKey="b_success_rate",
                type="network",
            ),
            Vis(title="Nodes beliefs", dataKey="b_success_rate", type="bar"),
            Vis(
                title="Nodes beliefs over time",
                dataKey="b_success_rate",
                type="line",
            ),
        ],
    ),
    Model(
        id="toni-akintola-boltzmann-wealth-model",
        username="toni-akintola",
        repo="boltzmann-wealth-model",
        categories=["wealth-model", "abm"],
        visualizations=[
            Vis(
                title='Nodes colored by their "wealth" parameter',
                dataKey="wealth",
                type="network",
            ),
            Vis(
                title="Wealth of each node at timestep t",
                dataKey="wealth",
                type="bar",
            ),
        ],
    ),
    # Model(
    #     id="toni-akintola-boltzmann-wealth-model",
    #     username="toni-akintola",
    #     repo="huang-trackrecords",
    #     categories=["bandit", "abm"],
    #     visualizations=[
    #         Vis(
    #             title="Wealth of each node at timestep t",
    #             dataKey="true_bias",
    #             type="bar",
    #         ),
    #     ],
    # ),
]


def getModels(filteredCategories: list[str] = []):
    """Returns all models tagged with at least one of the filteredCategories."""
    # Here, we use a lambda function to find all the models that are tagged with at least one of the filteredCategories
    model_data = (
        list(
            filter(
                lambda model: (
                    True
                    if len(
                        [
                            category
                            for category in model.categories
                            if category in filteredCategories
                        ]
                    )
                    > 0
                    else False
                ),
                models,
            )
        )
        if filteredCategories
        else models
    )
    data = {"models": model_data}
    return jsonpickle.encode(data)


def attribs(obj):
    return [
        o
        for o in dir(obj)
        if not o.startswith("_")
        and not inspect.ismethod(o)
        and not o
        in {
            "delete_parameters",
            "get_graph",
            "initial_data_function",
            "is_converged",
            "list_parameters",
            "run_to_convergence",
            "set_graph",
            "set_initial_data_function",
            "set_timestep_function",
            "timestep_function",
            "update_parameters",
            "initialize_graph",
            "timestep",
        }
    ]


def getGitHub(username: str, repo: str):
    """Given a username and repository path, returns the either raw code for a model file or a JSON object of the repository's data."""

    github_url = f"https://api.github.com/repos/{username}/{repo}"

    response = requests.get(github_url)
    data = response.json()

    return data


def timestep(graph, model: AgentModel, timesteps: int, run_to_convergence=False):
    mean_vals = []

    # Get all keys that have numerical values in the graph
    numerical_keys = {
        key
        for node, data in graph.nodes(data=True)
        for key in data
        if isinstance(data[key], (int, float, complex))
    }

    for _ in range(timesteps):
        model.timestep()
        updated_graph = model.get_graph()
        timestep_means = {}
        for key in numerical_keys:
            values = [
                data[key]
                for node, data in updated_graph.nodes(data=True)
                if key in data and data[key] is not None
            ]
            new_mean = statistics.mean(values) if values else 0
            timestep_means[key] = new_mean
        mean_vals.append(timestep_means)

    if run_to_convergence:
        t = 0
        while t < model["MAX_TIMESTEPS"] and not model.is_converged(
            data_key=model["convergence_data_key"], std_dev=model["convergence_std_dev"]
        ):
            model.timestep()
            updated_graph = model.get_graph()
            timestep_means = {}
            for key in numerical_keys:
                values = [
                    data[key]
                    for node, data in updated_graph.nodes(data=True)
                    if key in data and data[key] is not None
                ]
                new_mean = statistics.mean(values) if values else 0
                timestep_means[key] = new_mean
            mean_vals.append(timestep_means)
            t += 1
    final_graph = model.get_graph()
    nodes, edges = [node for node in final_graph.nodes(data=True)], [
        edge for edge in final_graph.edges(data=True)
    ]
    data = {"nodeData": nodes, "edgeData": edges, "meanVals": mean_vals}
    return data
