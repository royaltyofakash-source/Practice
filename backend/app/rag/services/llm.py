import os
from groq import Groq
from app.rag.services.prompts import build_system_prompt

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Please set it in your environment variables.")
    return Groq(api_key=api_key)

def generate_answer(question: str, context_chunks: list[str]) -> str:
    client = get_groq_client()

    context = "\n\n".join(context_chunks)

    print(f"DEBUG: Question: {question}")
    print(f"DEBUG: Context length: {len(context)} characters")
    print(f"DEBUG: Context preview: {context[:300]}...")

    system_prompt = build_system_prompt(context)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
        max_tokens=1000
    )

    answer = response.choices[0].message.content
    print(f"DEBUG: LLM Response: {answer[:200]}...")

    return answer
