def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start += chunk_size - overlap

    return chunks


def create_chunks(documents):
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["content"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "filename": doc["filename"],
                "chunk_id": i,
                "text": chunk
            })

    return all_chunks