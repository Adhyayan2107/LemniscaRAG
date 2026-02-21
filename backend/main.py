from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from backend.Rag import process_query
from backend.text_embedding.embedding import embed_chunks
from backend.text_chunking.text_splitter_langchain import split_documents
from backend.text_chunking.loadingdata import load_documents
from backend.vector_store.vector_store import save_chunks, load_chunks
from dotenv import load_dotenv
import uuid
import os

load_dotenv()

chunks = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global chunks

    VECTOR_STORE_PATH = os.path.join(os.getcwd(), "vector_store.pkl")
    DOCS_PATH = os.path.join(os.getcwd(), "clearpath_docs")

    print("CWD:", os.getcwd())
    print("Vector path:", VECTOR_STORE_PATH)
    print("Vector exists:", os.path.exists(VECTOR_STORE_PATH))

    if os.path.exists(VECTOR_STORE_PATH):
        chunks = load_chunks(VECTOR_STORE_PATH)
        print("Loaded saved embeddings")
    else:
        print("Vector store missing — creating embeddings")
        documents = load_documents(DOCS_PATH)
        chunks_split = split_documents(documents)
        chunks_embedded = embed_chunks(chunks_split)
        save_chunks(chunks_embedded, VECTOR_STORE_PATH)
        chunks = chunks_embedded
        print("Created embeddings")

    yield


app = FastAPI(lifespan=lifespan)


class QueryRequest(BaseModel):
    question: str
    conversation_id: str | None = None


@app.post("/query")
def query_endpoint(request: QueryRequest):
    conversation_id = request.conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
    result = process_query(request.question, chunks)
    result["conversation_id"] = conversation_id
    return result