import os
from io import BytesIO
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sentence_transformers import SentenceTransformer
from groq import Groq
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image



DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/authdb")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    conn.commit()

Base = declarative_base()



SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> list[float]:

    embedding = model.encode(text)
    return embedding.tolist()



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

    system_prompt = (
        "You are a helpful assistant. Answer the user's question based on the provided context. "
        "If the answer is in the context, provide a detailed response. "
        "If the information is not in the context, say 'I don't have enough information to answer this question.'\n\n"
        f"Context:\n{context}"
    )

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



def extract_text_from_image(image_bytes: bytes) -> str:
    image = Image.open(BytesIO(image_bytes))
    extracted = pytesseract.image_to_string(image)

    print(f"DEBUG: OCR extracted {len(extracted)} characters from image")
    print(f"DEBUG: OCR preview: {extracted[:200]}...")

    return extracted

def extract_text_from_scanned_pdf(pdf_bytes: bytes) -> str:
    pages = convert_from_bytes(pdf_bytes)

    page_texts = []
    for idx, page_image in enumerate(pages):
        page_text = pytesseract.image_to_string(page_image)
        page_texts.append(page_text)
        print(f"DEBUG: OCR page {idx + 1}/{len(pages)}: {len(page_text)} characters")

    full_text = "\n".join(page_texts)

    print(f"DEBUG: OCR extracted {len(full_text)} characters from {len(pages)} pages")
    print(f"DEBUG: OCR preview: {full_text[:200]}...")

    return full_text
