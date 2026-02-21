import numpy as np

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    return dot_product / (norm_vec1 * norm_vec2)


def retrieve_top_k(query, chunks, embedding_model, k=3):
    query_embedding = embedding_model.encode(query).tolist()

    scores = []

    for chunk in chunks:
        score = cosine_similarity(query_embedding, chunk["embedding"])
        scores.append((score, chunk))

    scores.sort(key=lambda x: x[0], reverse=True)

    top_chunks = [item[1] for item in scores[:k]]

    return top_chunks