import os
import shutil
import uuid

from dotenv import load_dotenv

from app.utils.config_loader import load_config
from app.ingestion.loader import load_documents
from app.ingestion.splitter import TextChunker
from app.ingestion.embedder import Embedder
from app.vectordb.chroma_client import ChromaDBClient

load_dotenv()

config = load_config()


def delete_existing_vectordb():

    persist_directory = config["vectordb"]["persist_directory"]

    if os.path.exists(persist_directory):

        shutil.rmtree(persist_directory)

        print("Old Vector DB Deleted")


def run_ingestion():

    print("Starting Ingestion Pipeline")

    delete_existing_vectordb()

    docs = load_documents("data/docs")

    chunker = TextChunker(
        chunk_size=config["chunking"]["chunk_size"],
        chunk_overlap=config["chunking"]["chunk_overlap"]
    )

    chunks = chunker.split(docs)

    texts = [chunk.page_content for chunk in chunks]

    embedder = Embedder(
        model_name=config["embedding"]["model_name"]
    )

    embeddings = embedder.embed_documents(texts)

    ids = [str(uuid.uuid4()) for _ in texts]

    chroma_client = ChromaDBClient(
        persist_directory=config["vectordb"]["persist_directory"],
        collection_name=config["vectordb"]["collection_name"]
    )

    chroma_client.add_documents(
        ids=ids,
        documents=texts,
        embeddings=embeddings
    )

    print("Vector DB Created Successfully")


if __name__ == "__main__":

    run_ingestion()