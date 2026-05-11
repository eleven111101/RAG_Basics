from langchain_openai import OpenAIEmbeddings


class Embedder:
    def __init__(self, model_name):
        self.embedding_model = OpenAIEmbeddings(model=model_name)

    def embed_documents(self, texts):
        return self.embedding_model.embed_documents(texts)

    def embed_query(self, query):
        return self.embedding_model.embed_query(query)