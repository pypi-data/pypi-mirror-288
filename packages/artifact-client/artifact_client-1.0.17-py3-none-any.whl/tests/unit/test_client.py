import unittest
from artifact_client.client import ArtifactClient


class TestArtifactClient(unittest.TestCase):

    def setUp(self):
        self.api_key = "0fa8f115-847f-4d25-a686-63aa1ed2b1ed"
        self.client = ArtifactClient(api_key=self.api_key)

    def test_create_graph(self):
        # Clear all graphs
        self.client.delete_all_graphs()

        graph = self.client.create_graph(name="TestGraph", index_interval="HOURLY")
        self.assertIsNotNone(graph)

    def test_create_graph_alternate(self):
        graph = self.client.Graph(name="TestGraph", index_interval="HOURLY")
        self.assertIsNotNone(graph)

    def test_list_graphs(self):
        graphs = self.client.list_graphs()
        self.assertIsNotNone(graphs)

    def test_ingest_document(self):
        graph = self.client.Graph(name="TestGraph")
        graph.ingest(document="sample document")


    def test_index_graph(self):
        graph = self.client.Graph(name="TestIndexGraph") # implicitly has "DAILY" indexing interval
        graph.ingest(document="This is a test document.")
        graph.index()

    def test_query_graph(self):
        graph = self.client.Graph(name="TestGraph")
        result = graph.query(query="Test query")

        self.assertIsNotNone(result)

    def test_get_graph_stats(self):
        graph = self.client.Graph(name="TestGraph")
        stats = graph.stats()

        self.assertEqual(stats.edge_count, 0)
        self.assertEqual(stats.node_count, 0)

    def test_get_graph_documents_meta(self):
        graph = self.client.Graph(name="TestGraph")
        graph.ingest(document="sample document")

        documents_meta = graph.documents_meta()

        print(documents_meta)

        self.assertIsNotNone(documents_meta)

    def test_delete_graph(self):
        self.client.delete_all_graphs()

        # Check that we are starting from a clean slate
        graphs = self.client.list_graphs()
        self.assertEqual(len(graphs), 0)

        graph1 = self.client.Graph(name="TestGraphForDeletion")

        # Check that graph was created
        graphs = self.client.list_graphs()
        self.assertEqual(len(graphs), 1)

        graph1.delete()

        # Check that graph was deleted
        graphs = self.client.list_graphs()
        self.assertEqual(len(graphs), 0)

    def test_delete_all_graphs(self):
        self.client.delete_all_graphs()

        # Check that we are starting from a clean slate
        graphs = self.client.list_graphs()
        self.assertEqual(len(graphs), 0)

        self.client.delete_all_graphs()

        self.client.Graph(name="TestGraph1")
        self.client.Graph(name="TestGraph2")

        # Check that graphs were created
        graphs = self.client.list_graphs()
        self.assertEqual(len(graphs), 2)

        self.client.delete_all_graphs()

        # Check that graph was deleted
        graphs = self.client.list_graphs()
        self.assertEqual(len(graphs), 0)

if __name__ == '__main__':
    unittest.main()