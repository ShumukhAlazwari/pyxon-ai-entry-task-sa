import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, insert_document,get_all_documents

from loader import load_document
from rag import (
    choose_chunking,
    store_chunks,
    retrieve_chunks,
    generate_answer,
    clear_collection,
)

app = FastAPI()
init_db()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "AI Document Analyzer is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected.")

    allowed_extensions = (".pdf", ".docx", ".txt")
    if not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload PDF, DOCX, or TXT."
        )

    file_path = os.path.join(DATA_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        text = load_document(file_path)
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from the document.")

        chunks = choose_chunking(text)
        clear_collection()
        stored_count = store_chunks(chunks, source_file=file.filename)

        filetype = file.filename.split(".")[-1]

        insert_document(
            filename=file.filename,
            filetype=filetype,
            chunks=stored_count
        )

        return {
            "message": "File uploaded and processed successfully.",
            "filename": file.filename,
            "chunks": stored_count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/ask")
def ask(q: str):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    retrieved = retrieve_chunks(q)
    answer = generate_answer(q, retrieved)

    return {
        "question": q,
        "answer": answer
    }

@app.get("/documents")
def documents():
    rows = get_all_documents()

    formatted = []
    for r in rows:
        formatted.append({
            "id": r[0],
            "filename": r[1],
            "filetype": r[2],
            "chunks": r[3],
            "upload_time": r[4]
        })

    return {"data": formatted}