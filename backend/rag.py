from typing import List
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import re
import uuid
import chromadb



model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="documents")


def clean_text(text: str) -> str:
    if not text:
        return ""

    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    text = "\n".join(lines)

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def fixed_chunk(text: str, chunk_size: int = 150, overlap: int = 30):
    text = clean_text(text)
    chunks = []

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def dynamic_chunk(text: str, max_chunk_size: int = 150) -> list[str]:
    text = clean_text(text)
    paragraphs = text.split("\n")

    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) + 1 <= max_chunk_size:
            current_chunk += para + "\n"
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def choose_chunking(text: str) -> List[str]:
    text = clean_text(text)

    if "\n" in text and len(text.split("\n")) > 3:
        return dynamic_chunk(text)

    return fixed_chunk(text)


def clear_collection() -> None:
    global collection
    try:
        client.delete_collection(name="documents")
    except Exception:
        pass

    collection = client.get_or_create_collection(name="documents")


def store_chunks(chunks: List[str], source_file: str = "uploaded_file") -> int:
    if not chunks:
        return 0

    embeddings = model.encode(chunks).tolist()

    ids = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(str(uuid.uuid4()))
        metadatas.append({
            "source_file": source_file,
            "chunk_index": i
        })

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)


def retrieve_chunks(query: str, top_k: int = 1) -> list[str]:
    query = clean_text(query)
    if not query:
        return []

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [])
    if not documents or not documents[0]:
        return []

    return documents[0]

def format_arabic_for_display(text: str, line_length: int = 90) -> str:

    text = clean_text(text)
    words = text.split()
    if not words:
        return ""

    lines = []
    current_line = ""

    for word in words:
        candidate = f"{current_line} {word}".strip()
        if len(candidate) <= line_length:
            current_line = candidate
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return "\n".join(lines)


def generate_answer(query: str, retrieved_chunks: List[str]) -> str:
    if not retrieved_chunks:
        return "لم يتم العثور على معلومات مناسبة في المستند."

    context = "\n\n".join(retrieved_chunks[:2])
    context = format_arabic_for_display(context)

    return f"إجابة مستندة إلى المستند:\n\n{context}"