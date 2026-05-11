from app.ingestion.embedder import Embedder
from app.vectordb.chroma_client import ChromaDBClient


class Retriever:
    def __init__(self, config):
        self.embedder = Embedder(
            model_name=config["embedding"]["model_name"]
        )

        self.db = ChromaDBClient(
            persist_directory=config["vectordb"]["persist_directory"],
            collection_name=config["vectordb"]["collection_name"]
        )

        self.top_k = config["retrieval"]["top_k"]

    def retrieve(self, query):
        query_embedding = self.embedder.embed_query(query)

        results = self.db.query(
            query_embedding=query_embedding,
            top_k=self.top_k
        )

        return results["documents"][0]