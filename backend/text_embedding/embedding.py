from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    embedding = embedding_model.encode(text)
    return embedding.tolist()


def embed_chunks(chunks):
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedding_model.encode(texts)
    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist()

    return chunks