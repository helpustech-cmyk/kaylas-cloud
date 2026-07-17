from pydantic import BaseModel, EmailStr
from typing import Optional


class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    country_code: Optional[str] = "+91"
    company: Optional[str] = None
    source: Optional[str] = "website"
    message: Optional[str] = None


class LeadResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    country_code: Optional[str] = "+91"
    status: str
    created_at: str

    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    session_id: str
    messages: list[ChatMessage]


class ChatResponse(BaseModel):
    role: str = "assistant"
    content: str
    sources: Optional[list[dict]] = None


class ContentCreate(BaseModel):
    slug: str
    title: str
    type: str  # blog, research, case_study
    content_md: str
    excerpt: Optional[str] = None
    series: Optional[str] = None
    series_order: Optional[int] = None
    status: str = "draft"


class ContentItem(BaseModel):
    slug: str
    title: str
    type: str
    excerpt: Optional[str]
    series: Optional[str]
    published_at: Optional[str]
    status: str


class AnalyticsEventCreate(BaseModel):
    event_name: str
    path: Optional[str] = None
    referrer: Optional[str] = None
    session_id: Optional[str] = None
    meta: Optional[dict] = None


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: dict

class StatsResponse(BaseModel):
    uptime_days: float
    published_posts: int
    total_leads: int
    last_publish: Optional[str] = None
    services_running: int
