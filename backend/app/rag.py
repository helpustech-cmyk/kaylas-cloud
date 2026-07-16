import os
import re
from typing import Optional

import httpx
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import Document

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """Simple overlap chunking by paragraphs."""
    paragraphs = re.split(r"\n\s*\n", text.strip())
    chunks = []
    current = ""
    for p in paragraphs:
        if len(current) + len(p) > chunk_size and current:
            chunks.append(current.strip())
            current = current[-overlap:] if len(current) > overlap else ""
        current += "\n\n" + p if current else p
    if current:
        chunks.append(current.strip())
    return chunks or [text]


async def embed_text(text: str) -> list[float]:
    payload = {"model": EMBED_MODEL, "prompt": text}
    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(f"{OLLAMA_HOST}/api/embeddings", json=payload)
        res.raise_for_status()
        data = res.json()
        return data["embedding"]


def get_embedding_sql(vector: list[float]) -> str:
    return "[" + ",".join(str(v) for v in vector) + "]"


def ensure_chunks_table(db: Session):
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
            chunk_index INT NOT NULL,
            content TEXT NOT NULL,
            embedding vector(768)
        );
        CREATE INDEX IF NOT EXISTS idx_document_chunks_embedding
        ON document_chunks USING ivfflat (embedding vector_l2_ops);
    """))
    db.commit()


async def index_document(db: Session, doc: Document):
    """Chunk and store document embeddings in pgvector."""
    ensure_chunks_table(db)
    # Clear old chunks
    db.execute(text("DELETE FROM document_chunks WHERE document_id = :did"), {"did": str(doc.id)})

    chunks = chunk_text(doc.content_md)
    for i, chunk in enumerate(chunks):
        vector = await embed_text(chunk)
        db.execute(
            text("""
                INSERT INTO document_chunks (id, document_id, chunk_index, content, embedding)
                VALUES (gen_random_uuid(), :document_id, :chunk_index, :content, CAST(:embedding AS vector))
            """),
            {
                "document_id": str(doc.id),
                "chunk_index": i,
                "content": chunk,
                "embedding": get_embedding_sql(vector),
            },
        )
    db.commit()


async def search_documents(db: Session, query: str, top_k: int = 4) -> list[dict]:
    ensure_chunks_table(db)
    vector = await embed_text(query)
    sql = text("""
        SELECT d.slug, d.title, d.type, dc.content, dc.chunk_index,
               dc.embedding <-> CAST(:embedding AS vector) AS distance
        FROM document_chunks dc
        JOIN documents d ON d.id = dc.document_id
        WHERE d.status = 'published'
        ORDER BY dc.embedding <-> CAST(:embedding AS vector)
        LIMIT :limit
    """)
    rows = db.execute(sql, {"embedding": get_embedding_sql(vector), "limit": top_k}).fetchall()
    return [
        {
            "slug": r.slug,
            "title": r.title,
            "type": r.type,
            "content": r.content,
            "distance": r.distance,
        }
        for r in rows
    ]
