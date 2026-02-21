import time
from backend.Evaluations.router import classify_query
from backend.Similarity_search.similarity import retrieve_top_k
from backend.prompt_llm.prompting import build_prompt
from backend.prompt_llm.llm import generate_answer
from backend.text_embedding.embedding import embedding_model

CONFIDENCE_THRESHOLD = 0.35
MINIMUM_THRESHOLD = 0.20


def process_query(question, chunks):
    start_time = time.time()
    classification = classify_query(question)

    model_used = (
        "llama-3.3-70b-versatile"
        if classification == "complex"
        else "llama-3.1-8b-instant"
    )

    retrieved = retrieve_top_k(question, chunks, embedding_model, k=4)

    if not retrieved:
        return {
            "answer": "No relevant information found.",
            "metadata": {
                "model_used": model_used,
                "classification": classification,
                "chunks_retrieved": 0,
                "latency_ms": int((time.time() - start_time) * 1000),
                "evaluator_flags": ["no_context"]
            },
            "sources": []
        }

    top_score = retrieved[0][0]

    if top_score < MINIMUM_THRESHOLD:
        return {
            "answer": "Low confidence — please verify with support.",
            "metadata": {
                "model_used": model_used,
                "classification": classification,
                "chunks_retrieved": len(retrieved),
                "latency_ms": int((time.time() - start_time) * 1000),
                "evaluator_flags": ["no_context"]
            },
            "sources": []
        }

    top_chunks = [item[1] for item in retrieved]
    prompt = build_prompt(question, top_chunks)
    answer, tokens = generate_answer(prompt, model=model_used)
    latency = int((time.time() - start_time) * 1000)

    return {
        "answer": answer,
        "metadata": {
            "model_used": model_used,
            "classification": classification,
            "tokens": tokens,
            "chunks_retrieved": len(top_chunks),
            "latency_ms": latency,
            "evaluator_flags": []
        },
        "sources": [
            {
                "document": chunk["filename"],
                "page": 1,
                "relevance_score": round(score, 2)
            }
            for score, chunk in retrieved
        ]
    }