from typing import List

from artifact_client.models.graph_stats import GraphStats
from artifact_client.models.document_meta import DocumentMeta
from artifact_client.models.ingest_document_request import IngestDocumentRequest
from artifact_client.models.query_request import QueryRequest


class Graph:
    def __init__(self, artifact_client: 'ArtifactClient', name: str = None, uuid: str = None, index_interval: str = "IMMEDIATE"):
        self.artifact_client = artifact_client
        self.name = name
        self.index_interval = index_interval
        self.uuid = uuid

    def ingest(self, document: str) -> None:
        """Ingest a document into the graph."""
        body = IngestDocumentRequest(document=document)
        headers = self.artifact_client.set_auth_headers()
        return self.artifact_client.api_instance.ingest_document(graph_id=self.uuid, ingest_document_request=body, _headers=headers)

    def index(self) -> None:
        """Index the graph."""
        headers = self.artifact_client.set_auth_headers()
        return self.artifact_client.api_instance.index_graph(graph_id=self.uuid, _headers=headers)

    def query(self, query: str) -> str:
        """Query the graph."""
        body = QueryRequest(query=query)
        headers = self.artifact_client.set_auth_headers()
        return self.artifact_client.api_instance.query_graph(graph_id=self.uuid, query_request=body, _headers=headers).result

    def stats(self) -> GraphStats:
        """Get graph statistics."""
        headers = self.artifact_client.set_auth_headers()
        return self.artifact_client.api_instance.get_graph_stats(graph_id=self.uuid, _headers=headers)

    def documents_meta(self) -> List[DocumentMeta]:
        """Get documents metadata."""
        headers = self.artifact_client.set_auth_headers()
        return self.artifact_client.api_instance.get_graph_documents_meta(graph_id=self.uuid, _headers=headers)

    def delete(self) -> None:
        """Delete a graph."""
        headers = self.artifact_client.set_auth_headers()
        response = self.artifact_client.api_instance.delete_graph(graph_id=self.uuid, _headers=headers)
        return response