from langchain_openai import ChatOpenAI


class Generator:
    def __init__(self, config):
        self.llm = ChatOpenAI(
            model=config["llm"]["model_name"],
            temperature=config["llm"]["temperature"],
            max_tokens=config["llm"]["max_tokens"]
        )

    def generate(self, query, context):
        prompt = f"""
You are a helpful QnA assistant.

Context:
{context}

Question:
{query}

Answer:
"""

        response = self.llm.invoke(prompt)

        return response.content