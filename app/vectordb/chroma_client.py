import chromadb
from chromadb.config import Settings


class ChromaDBClient:
    def __init__(self, persist_directory, collection_name):
        self.client = chromadb.PersistentClient(path=persist_directory)

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_documents(self, ids, documents, embeddings):
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings
        )

    def query(self, query_embedding, top_k=4):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )