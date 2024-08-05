from typing import List, Optional

from artifact_client.api import default_api

from models.graph import Graph
from artifact_client.models.create_graph_request import CreateGraphRequest
from artifact_client.configuration import Configuration
from artifact_client.api_client import ApiClient


class ArtifactClient:
    def __init__(self, api_key: str, base_url: str = "https://xxny160gbe.execute-api.us-east-1.amazonaws.com/Prod"):
        # Configure the client
        config = Configuration(host=base_url)
        config.api_key = {"Authorization": api_key}
        config.api_key_prefix['Authorization'] = 'Bearer'
        self.client = ApiClient(configuration=config)
        self.api_instance = default_api.DefaultApi(api_client=self.client)
        self.api_key = api_key

    def set_auth_headers(self):
        """Set the Authorization header."""
        headers = {'Authorization': f'{self.api_key}'}
        return headers

    def Graph(self, name: str = None, graph_id: str = None, index_interval: str = "IMMEDIATE") -> Graph:
        """Retrieve or create a graph."""
        if graph_id:
            # Connect to an existing graph
            return Graph(self, uuid=graph_id)
        elif name:
            # List all graphs and check if one with the given name already exists
            try:
                graphs = self.list_graphs()
                for graph in graphs:
                    if graph.name == name:
                        # Create from Graph object
                        return Graph(self, uuid=graph.uuid, name=graph.name)
                # If no graph with the given name exists, create a new one
                new_graph = self.create_graph(name=name, index_interval=index_interval)
                return Graph(self, uuid=new_graph.uuid, name=new_graph.name)
            except Exception as e:
                print(f"Exception during graph retrieval or creation: {e}")
                raise
        else:
            raise ValueError("Either 'name' or 'graph_id' must be provided to retrieve or create a graph.")

    def create_graph(self, name: str, index_interval: str = "IMMEDIATE") -> Graph:
        """Create a new graph."""
        body = CreateGraphRequest(name=name, index_interval=index_interval)
        headers = self.set_auth_headers()
        new_graph = self.api_instance.create_graph(create_graph_request=body, _headers=headers)
        return Graph(self, uuid=new_graph.uuid, name=new_graph.name, index_interval=new_graph.index_interval)

    def delete_all_graphs(self) -> None:
        """Delete a graph."""
        headers = self.set_auth_headers()
        response = self.api_instance.delete_all_graphs(_headers=headers)
        return response

    def list_graphs(self) -> List[Graph]:
        """Lists all graphs."""
        headers = self.set_auth_headers()
        response = self.api_instance.list_graphs(_headers=headers)
        return response

    def _get_graph_id_by_name(self, name: str) -> Optional[str]:
        """Retrieve the graph ID by its name."""
        graphs = self.list_graphs()
        for graph in graphs:
            if graph.name == name:
                return graph.id
        return None
