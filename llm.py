from groq import Groq
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def generate_answer(prompt, model="llama-3.1-8b-instant"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a precise and factual assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content