from fastapi import FastAPI
from pydantic import BaseModel
from backend.Rag import process_query
from dotenv import load_dotenv
import uuid

load_dotenv()
app = FastAPI()

from backend.text_embedding.embedding import embed_chunks
from backend.text_chunking.text_splitter_langchain import split_documents
from backend.text_chunking.loadingdata import load_documents
from backend.vector_store.vector_store import save_chunks, load_chunks
import os

if os.path.exists("/Users/adhyayan/PycharmProjects/LemniscaRAG/backend/vector_store/vector_store.pkl"):
    chunks = load_chunks()
    print("Loaded saved embeddings")
else:
    documents = load_documents('/Users/adhyayan/PycharmProjects/LemniscaRAG/clearpath_docs')
    chunks = split_documents(documents)
    chunks = embed_chunks(chunks)
    save_chunks(chunks)
    print("Created embeddings")

class QueryRequest(BaseModel):
    question: str
    conversation_id: str | None = None


@app.post("/query")
def query_endpoint(request: QueryRequest):
    conversation_id = request.conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
    result = process_query(request.question, chunks)
    result["conversation_id"] = conversation_id
    return result