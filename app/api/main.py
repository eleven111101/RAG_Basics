from fastapi import FastAPI
from dotenv import load_dotenv

from app.models.schemas import QueryRequest
from app.qna.pipeline import QnAPipeline
from app.ingestion.ingest import run_ingestion

load_dotenv()

app = FastAPI(title="RAG QnA Bot")

pipeline = QnAPipeline()


@app.get("/")
def health_check():

    return {
        "status": "running"
    }


@app.post("/ingest")
def ingest_documents():

    run_ingestion()

    return {
        "status": "success",
        "message": "Vector DB created successfully"
    }


@app.post("/ask")
def ask_question(request: QueryRequest):

    response = pipeline.ask(request.question)

    return {
        "answer": response["answer"],
        "context": response["context"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}