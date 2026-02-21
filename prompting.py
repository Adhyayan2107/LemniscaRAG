def build_prompt(query, retrieved_chunks):
    context = "\n\n".join(
        [chunk["text"] for chunk in retrieved_chunks]
    )

    prompt = f"""
        You are a helpful assistant answering questions strictly using the provided context.
        
        If the answer is not found in the context, say:
        "I cannot find this information in the provided documents."
        
        Context:
        {context}
        
        Question:
        {query}
        
        Answer:
    """
    return prompt