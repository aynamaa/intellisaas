from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.models.document import Document
from app.services.document_service import save_upload_file, extract_text
from app.services.ai_service import summarize_document, chat_with_document
from pydantic import BaseModel

router = APIRouter(prefix="/documents", tags=["documents"])

ALLOWED_TYPES = ["pdf", "docx", "txt", "doc"]

class ChatRequest(BaseModel):
    question: str

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"File type .{ext} not allowed. Use PDF, DOCX, or TXT.")

    unique_name, file_path, file_size = await save_upload_file(file)
    text_content = extract_text(file_path, ext)
    summary = await summarize_document(text_content)

    doc = Document(
        user_id=current_user["sub"],
        filename=unique_name,
        original_name=file.filename,
        file_type=ext,
        file_size=file_size,
        content=text_content,
        summary=summary,
        status="ready"
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    return {
        "id": str(doc.id),
        "filename": doc.original_name,
        "summary": doc.summary,
        "status": doc.status,
        "file_size": doc.file_size
    }

@router.get("/")
async def list_documents(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Document).where(Document.user_id == current_user["sub"])
    )
    docs = result.scalars().all()
    return [{"id": str(d.id), "filename": d.original_name,
             "file_type": d.file_type, "status": d.status,
             "summary": d.summary, "created_at": str(d.created_at)} for d in docs]

@router.get("/{doc_id}")
async def get_document(
    doc_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Document).where(Document.id == doc_id, Document.user_id == current_user["sub"])
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"id": str(doc.id), "filename": doc.original_name,
            "content": doc.content, "summary": doc.summary, "status": doc.status}

@router.post("/{doc_id}/chat")
async def chat_document(
    doc_id: str,
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Document).where(Document.id == doc_id, Document.user_id == current_user["sub"])
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    answer = await chat_with_document(doc.content, request.question)
    return {"question": request.question, "answer": answer, "document": doc.original_name}

@router.delete("/{doc_id}")
async def delete_document(
    doc_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Document).where(Document.id == doc_id, Document.user_id == current_user["sub"])
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    await db.delete(doc)
    await db.commit()
    return {"message": "Document deleted successfully"}