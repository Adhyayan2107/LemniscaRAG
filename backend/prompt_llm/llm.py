from groq import Groq
import os

def generate_answer(prompt, model="llama-3.1-8b-instant"):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Check .env loading.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a precise and factual assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    answer = response.choices[0].message.content

    tokens = {
        "input": response.usage.prompt_tokens,
        "output": response.usage.completion_tokens
    }

    return answer, tokens