import os
import hashlib
from io import BytesIO
from pypdf import PdfReader
from docx import Document as DocxDocument
from sqlalchemy.orm import Session
from app.rag.models import documentModels as document_model
from app.rag.services.embeddings import get_embedding
from app.rag.services.llm import generate_answer
from app.rag.services.ocr import extract_text_from_image, extract_text_from_scanned_pdf

def process_document(db: Session, user_id: int, filename: str, file_content: bytes):
    content_hash = hashlib.sha256(file_content).hexdigest()

    existing_doc = document_model.get_document_by_hash(db, user_id, content_hash)
    if existing_doc:
        raise ValueError(f"This document has already been uploaded (as '{existing_doc.filename}').")

    if filename.lower().endswith(".pdf"):
        reader = PdfReader(BytesIO(file_content))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    elif filename.lower().endswith(".docx"):
        doc = DocxDocument(BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"
    elif filename.lower().endswith(".txt"):
        text = file_content.decode("utf-8")
    elif filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        text = extract_text_from_image(file_content)
    else:
        # Try to decode as UTF-8 for other text files
        try:
            text = file_content.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError(f"Unsupported file format. Please upload PDF, DOCX, or TXT files.")
        
    # Scanned PDFs have no embedded text layer, so fall back to OCR
    if filename.lower().endswith(".pdf") and len(text.strip()) < 20:
        print("DEBUG: PDF has little or no embedded text, falling back to OCR")
        text = extract_text_from_scanned_pdf(file_content)

    if not text.strip():
        raise ValueError("No text content found in the document")
    
    print(f"DEBUG: Extracted text length: {len(text)} characters")
    print(f"DEBUG: Text preview: {text[:200]}...")
        
    chunk_size = 500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size) if text[i:i+chunk_size].strip()]
    
    print(f"DEBUG: Created {len(chunks)} chunks")
    
    doc_record = document_model.create_document(db, user_id, filename, content_hash)
    print(f"DEBUG: Created document with ID: {doc_record.id}")
    
    for idx, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        document_model.create_chunk(db, doc_record.id, chunk, embedding)
        if idx == 0:
            print(f"DEBUG: First chunk: {chunk[:100]}...")
            print(f"DEBUG: Embedding dimensions: {len(embedding)}")
    
    print(f"DEBUG: Successfully saved {len(chunks)} chunks to database")
        
    return doc_record

def answer_query(db: Session, user_id: int, question: str) -> str:
    query_embedding = get_embedding(question)
    chunks = document_model.search_similar_chunks(db, user_id, query_embedding)
    
    print(f"DEBUG: Found {len(chunks)} chunks for user {user_id}")
    if chunks:
        print(f"DEBUG: First chunk content preview: {chunks[0].content[:100]}...")
    
    if not chunks:
        return "Aapne abhi tak koi document upload nahi kiya"
        
    context_contents = [chunk.content for chunk in chunks]
    return generate_answer(question, context_contents)
