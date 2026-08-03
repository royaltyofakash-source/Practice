from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, Session
from datetime import datetime
from pgvector.sqlalchemy import Vector
from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    content_hash = Column(String, index=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    chunks = relationship("DocumentChunk", back_populates="document")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    content = Column(Text)
    embedding = Column(Vector(384))

    document = relationship("Document", back_populates="chunks")

def create_document(db: Session, user_id: int, filename: str, content_hash: str):
    new_doc = Document(user_id=user_id, filename=filename, content_hash=content_hash)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

def get_document_by_hash(db: Session, user_id: int, content_hash: str):
    return (
        db.query(Document)
        .filter(Document.user_id == user_id, Document.content_hash == content_hash)
        .first()
    )

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
