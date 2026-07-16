from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db_session
from app.models import Lead, Conversation, Document, AutomationLog, AnalyticsEvent
from app.schemas import LeadCreate, LeadResponse, ChatRequest, ChatResponse, ContentCreate, ContentItem, AnalyticsEventCreate, HealthResponse
from app.telegram import send_telegram_message, format_lead_alert
from app.llm import generate_chat_response, SYSTEM_PROMPT
from app.rag import search_documents

router = APIRouter()


def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()


@router.post("/leads", response_model=LeadResponse)
async def create_lead(lead: LeadCreate, request: Request, db: Session = Depends(get_db)):
    db_lead = Lead(
        name=lead.name,
        email=lead.email,
        company=lead.company,
        source=lead.source or "website",
        message=lead.message,
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)

    alert_text = format_lead_alert(
        name=lead.name,
        email=lead.email,
        company=lead.company,
        source=lead.source,
        message=lead.message,
    )
    try:
        await send_telegram_message(alert_text)
    except Exception:
        pass  # Don't fail the request if Telegram is down

    return LeadResponse(
        id=str(db_lead.id),
        name=db_lead.name,
        email=db_lead.email,
        status=db_lead.status,
        created_at=db_lead.created_at.isoformat() if db_lead.created_at else "",
    )


@router.post("/twin/chat", response_model=ChatResponse)
async def twin_chat(chat: ChatRequest, db: Session = Depends(get_db)):
    # Save user message
    user_msg = chat.messages[-1] if chat.messages else None
    if user_msg and user_msg.role == "user":
        db.add(Conversation(session_id=chat.session_id, role="user", content=user_msg.content))
        db.commit()

    # Retrieve context via RAG
    sources = []
    system_content = SYSTEM_PROMPT
    if user_msg:
        try:
            sources = await search_documents(db, user_msg.content, top_k=3)
            if sources:
                context = "\n\n".join([f"From {s['title']} ({s['type']}):\n{s['content']}" for s in sources])
                system_content += f"\n\nUse the following context to answer if relevant:\n{context}"
        except Exception:
            sources = []

    messages_for_llm = [{"role": "system", "content": system_content}]
    for m in chat.messages[-10:]:
        messages_for_llm.append({"role": m.role, "content": m.content})

    try:
        reply = await generate_chat_response(messages_for_llm)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    db.add(Conversation(session_id=chat.session_id, role="assistant", content=reply, sources=sources))
    db.commit()

    return ChatResponse(content=reply, sources=sources)


@router.get("/twin/history/{session_id}")
async def twin_history(session_id: str, db: Session = Depends(get_db)):
    convs = (
        db.query(Conversation)
        .filter(Conversation.session_id == session_id)
        .order_by(Conversation.created_at.asc())
        .all()
    )
    return [
        {"role": c.role, "content": c.content, "sources": c.sources, "created_at": c.created_at.isoformat()}
        for c in convs
    ]


@router.post("/content", response_model=ContentItem)
async def create_content(item: ContentCreate, db: Session = Depends(get_db)):
    existing = db.query(Document).filter(Document.slug == item.slug).first()
    if existing:
        raise HTTPException(status_code=409, detail="Slug already exists")

    doc = Document(
        slug=item.slug,
        title=item.title,
        type=item.type,
        content_md=item.content_md,
        excerpt=item.excerpt,
        series=item.series,
        series_order=item.series_order,
        status=item.status,
    )
    if item.status == "published":
        doc.published_at = datetime.now(timezone.utc)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return _content_to_schema(doc)


@router.get("/content", response_model=list[ContentItem])
async def list_content(type: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Document).filter(Document.status == "published")
    if type:
        q = q.filter(Document.type == type)
    docs = q.order_by(Document.published_at.desc()).all()
    return [_content_to_schema(d) for d in docs]


@router.get("/content/{slug}", response_model=ContentItem)
async def get_content(slug: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.slug == slug).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    return _content_to_schema(doc)


@router.post("/analytics/event")
async def track_event(event: AnalyticsEventCreate, db: Session = Depends(get_db)):
    db.add(AnalyticsEvent(
        event_name=event.event_name,
        path=event.path,
        referrer=event.referrer,
        session_id=event.session_id,
        meta=event.meta,
    ))
    db.commit()
    return {"ok": True}


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat(),
        services={"api": "ok", "database": "connected"},
    )


def _content_to_schema(doc: Document) -> ContentItem:
    return ContentItem(
        slug=doc.slug,
        title=doc.title,
        type=doc.type,
        excerpt=doc.excerpt,
        series=doc.series,
        published_at=doc.published_at.isoformat() if doc.published_at else None,
        status=doc.status,
    )
