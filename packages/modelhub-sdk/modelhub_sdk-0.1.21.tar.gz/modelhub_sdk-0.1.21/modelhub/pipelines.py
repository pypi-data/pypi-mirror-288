import os
import requests
import yaml
import networkx as nx
from modelhub.models import PipelineCreateRequest
import base64
from modelhub.client import ModelHub
from modelhub.utils.logger import setup_logger

logger = setup_logger(__name__)

class Pipeline:
    """A class to create and manage machine learning pipelines on ModelHub."""

    def __init__(self, client: ModelHub, config_path):
        self.client = client
        self.config_path = config_path
        self.pipeline_request = self.load_config(config_path)

    def load_config(self, config_path):
        """Load pipeline configuration from a YAML file."""
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        for stage in config["stages"]:
            if "script" in stage and stage["script"]:
                stage["script"] = self.encode_file(stage["script"])
            if "requirements" in stage and stage["requirements"]:
                stage["requirements"] = self.encode_file(stage["requirements"])

        return PipelineCreateRequest(**config)

    def encode_file(self, file_path):
        """Encode the contents of a file in Base64."""
        with open(file_path, "rb") as file:
            encoded = base64.b64encode(file.read()).decode("utf-8")
        return encoded

    def search_pipeline(self, name):
        """
        Searches for a pipeline with the given name.

        Args:
            name (str): The name of the pipeline to search for.

        Returns:
            dict or None: The existing pipeline if found, or None if not found.

        Raises:
            requests.exceptions.HTTPError: If an HTTP error occurs.
            requests.exceptions.RequestException: If a general request error occurs.
        """
        try:
            existing_pipeline = self.client.get(f"pipelines/search?name={name}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                existing_pipeline = None
            else:
                logger.error("HTTP error: %s", e.response.text)
                raise
        except requests.exceptions.RequestException as e:
            logger.error("Request error: %s", str(e))
            raise
        return existing_pipeline
    
    def create_or_update(self):
        """Create or update a pipeline based on the configuration."""
        existing_pipeline = self.search_pipeline(
            self.pipeline_request.name
        )
        if existing_pipeline:
            return self.client.put(
                f"pipelines/{existing_pipeline['pipeline_id']}",
                json=self.pipeline_request.dict(),
            )
        else:
            logger.info("Creating a new pipeline...")
            return self.client.post(
                "pipelines", json=self.pipeline_request.dict()
            )

    def submit(self):
        response = self.create_or_update()
        pipeline_id = response["pipeline_id"]
        return self.client.post(f"pipelines/{pipeline_id}/submit")

    def generate_dag_view(self):
        stages = self.pipeline_request.stages
        G = nx.DiGraph()

        for stage in stages:
            G.add_node(stage.name)
            for dependency in stage.depends_on:
                G.add_edge(dependency, stage.name)

        try:
            from networkx.drawing.nx_agraph import graphviz_layout
            import matplotlib.pyplot as plt
            from matplotlib import get_backend

            # Ensure the matplotlib backend is set correctly
            if get_backend() != "module://matplotlib_inline.backend_inline":
                plt.switch_backend("module://matplotlib_inline.backend_inline")

            pos = graphviz_layout(G, prog="dot")
            plt.figure(figsize=(12, 8))
            nx.draw(
                G,
                pos,
                with_labels=True,
                node_size=3000,
                node_color="lightblue",
                font_size=10,
                font_weight="bold",
                arrows=True,
                arrowsize=20,
            )
            plt.show()
        except ImportError:
            print(
                "matplotlib and pygraphviz are required for DAG visualization. Please install them using 'pip install matplotlib pygraphviz'."
            )

    def inspect(self):
        """Inspect the pipeline configuration."""
        self.generate_dag_view()
