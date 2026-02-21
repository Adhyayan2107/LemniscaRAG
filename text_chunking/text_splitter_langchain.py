from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,      # characters, not words
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""]
    )

    all_chunks = []

    for doc in documents:
        chunks = splitter.split_text(doc["content"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "filename": doc["filename"],
                "chunk_id": i,
                "text": chunk
            })

    return all_chunks