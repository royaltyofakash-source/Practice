from sqlalchemy.orm import Session
from app.auth.models.document import Document, DocumentChunk

def create_document(db: Session, user_id: int, filename: str):
    new_doc = Document(user_id=user_id, filename=filename)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

def create_chunk(db: Session, document_id: int, content: str, embedding: list[float]):
    new_chunk = DocumentChunk(document_id=document_id, content=content, embedding=embedding)
    db.add(new_chunk)
    db.commit()
    db.refresh(new_chunk)
    return new_chunk

def get_documents_by_user(db: Session, user_id: int):
    return db.query(Document).filter(Document.user_id == user_id).all()

def get_chunks_by_user(db: Session, user_id: int):
    return db.query(DocumentChunk).join(Document).filter(Document.user_id == user_id).all()

def search_similar_chunks(db: Session, user_id: int, query_embedding: list[float], top_k: int = 5):
    return (
        db.query(DocumentChunk)
        .join(Document)
        .filter(Document.user_id == user_id)
        .order_by(DocumentChunk.embedding.l2_distance(query_embedding))
        .limit(top_k)
        .all()
    )
