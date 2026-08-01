import os
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.shared.database.session import get_db
from app.auth.dependencies import get_current_user
from app.auth.services import document_service
from app.auth.repositories import document_repository
from app.auth.schemas.request import QueryRequest

router = APIRouter(prefix="/documents")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        content = await file.read()
        
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(content)
            
        doc = document_service.process_document(db, current_user.id, file.filename, content)
        return {"id": doc.id, "filename": doc.filename}
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

@router.get("/list")
def list_documents(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    docs = document_repository.get_documents_by_user(db, current_user.id)
    return [{"id": d.id, "filename": d.filename, "uploaded_at": d.uploaded_at} for d in docs]

@router.post("/query")
def query_documents(
    request: QueryRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        answer = document_service.answer_query(db, current_user.id, request.question)
        return {"answer": answer}
    except Exception as e:
        print(f"ERROR in query_documents: {str(e)}")
        import traceback
        traceback.print_exc()
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Failed to query documents: {str(e)}")
