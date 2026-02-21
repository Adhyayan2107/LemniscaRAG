from fastapi import FastAPI
from pydantic import BaseModel
from backend.Rag import process_query
from dotenv import load_dotenv
import uuid
import os

load_dotenv()

app = FastAPI()

from backend.text_embedding.embedding import embed_chunks
from backend.text_chunking.text_splitter_langchain import split_documents
from backend.text_chunking.loadingdata import load_documents
from backend.vector_store.vector_store import save_chunks, load_chunks

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR_STORE_PATH = os.path.join(BASE_DIR, "vector_store.pkl")
DOCS_PATH = os.path.join(BASE_DIR, "clearpath_docs")

print("Vector path:", VECTOR_STORE_PATH)
print("Vector exists:", os.path.exists(VECTOR_STORE_PATH))

if os.path.exists(VECTOR_STORE_PATH):
    chunks = load_chunks(VECTOR_STORE_PATH)
    print("Loaded saved embeddings")

else:
    print("Vector store not found!")
    raise Exception("vector_store.pkl missing")

class QueryRequest(BaseModel):
    question: str
    conversation_id: str | None = None

@app.post("/query")
def query_endpoint(request: QueryRequest):
    conversation_id = request.conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
    result = process_query(request.question, chunks)
    result["conversation_id"] = conversation_id
    return result