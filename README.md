# AI Document Analyzer (RAG System)

## 👩‍💻 Contact Information
Email: shumoukh88@gmail.com
 Phone:0501889546

---

## 🚀 Demo
Live demo:
(Add your link here later)

---

## 📌 Overview
This project implements a Retrieval-Augmented Generation (RAG) system that allows users to upload documents and ask questions about their content.

It supports Arabic documents and includes OCR fallback for corrupted PDF text.

---

## ⚙️ Features
- Upload documents (PDF, DOCX, TXT)
- Arabic support
- OCR fallback for broken PDFs
- Intelligent chunking (fixed + dynamic)
- Vector search using ChromaDB
- Metadata storage using SQLite
- Simple frontend interface
- Benchmark evaluation

---

## 🧠 Architecture
- FastAPI → backend API
- ChromaDB → vector database
- SQLite → metadata storage
- Sentence Transformers → embeddings
- EasyOCR → Arabic OCR fallback
- HTML/CSS/JS → frontend

---

## 🔄 Workflow
1. Upload document
2. Extract text
3. Split into chunks
4. Store embeddings
5. Ask question
6. Retrieve relevant chunks
7. Return answer

---

## 🧪 Benchmark
Run:cd backend
python benchmark.py

Example result:
{'accuracy': 1.0, 'details': [{'question': 'كم مدة العقد؟', 'score': 1}, {'question': 'عدد ساعات العمل', 'score': 1}]}

---

## ⚖️ Decisions & Trade-offs
- Used SQLite for simplicity and lightweight storage
- Used ChromaDB for local vector search
- Single active document to simplify retrieval
- OCR fallback for better Arabic PDF handling
- No LLM used (retrieval-based answers only)

---

## ❗ Assumptions
- Only one document is active at a time
- Storage is temporary in deployed demo
- Users will upload their own documents for testing

---

## ⚠️ Limitations
- No LLM-based answer generation
- OCR accuracy depends on PDF quality
- No multi-document support

---

## 🔮 Future Improvements
- Add LLM (OpenAI or local model)
- Improve ranking
- Support multiple documents
- Better evaluation metrics

---

## ▶️ How to Run

### Backend
cd backend
uvicorn main:app --reload

### Frontend
cd frontend
python -m http.server 5500

Open:http://127.0.0.1:5500