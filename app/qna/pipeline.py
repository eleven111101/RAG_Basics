from app.utils.config_loader import load_config
from app.qna.retriever import Retriever
from app.qna.generator import Generator


class QnAPipeline:
    def __init__(self):
        self.config = load_config()
        self.retriever = Retriever(self.config)
        self.generator = Generator(self.config)

    def ask(self, query):
        docs = self.retriever.retrieve(query)

        context = "\n\n".join(docs)

        answer = self.generator.generate(query, context)

        return {
            "query": query,
            "context": docs,
            "answer": answer
        }