#!/usr/bin/env python3
"""Seed the knowledge base with Kailas's core content."""

import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_db_session, init_db
from app.models import Document


CORE_DOCUMENTS = [
    {
        "slug": "about-kailas",
        "title": "About Kailas Swami",
        "type": "case_study",
        "content_md": """# About Kailas Swami

Kailas Sadanand Swami is a Digital Revenue Lead at Quick Heal, India's leading cybersecurity company.

## Core philosophy
Service + AI is the new operating system for customer experience. The next decade belongs to leaders who can blend operational rigor with AI-native thinking.

## Career arc
- Quick Heal — Digital Revenue Lead (Sept 2025 - Present)
- Parag Milk Foods — Head Customer Service (Dec 2024 - Sept 2025)
- L&T Finance — Manager Customer Service (Sept 2022 - Dec 2024)
- IDFC FIRST Bank — Team Leader, HNI video banking (Sept 2019 - Sept 2022)
- Trek Leader at Ultimate Hikers (volunteer, 2014 - Present)

## Education
- MBA, Suresh Gyan Vihar University (2023, CGPA 7.8)
- B.Com, K.G. Joshi & N.G. Bedekar College of Commerce (2018)

## Certifications
PMP Training, Lean Management, Start-Up Management. Pursuing Six Sigma Green Belt and Data Science with Python.

## Achievements
- Service level improved 21% to 96%
- Repeat calls reduced from 33% to 17%
- Attrition reduced from 11.2% to 5.8%
- Home-loan retention improved from 49% to 76%
- 58 SOPs authored
- Zero audit discrepancies across 8+ vendors
- 38 workflow gaps closed with digital solutions, 26% faster resolution

## What he builds
AI agents, n8n workflows, Python/Flask systems, Docker deployments, RPA, CRM and telephony automation, revenue operations, and business infrastructure strategy.

## Contact
- Email: kailashjd@outlook.com
- Phone: +91 9372133356
- LinkedIn: linkedin.com/in/kailash-swami-66a68015a
- Location: Nerul, Navi Mumbai, India
""",
        "excerpt": "Digital Revenue Lead at Quick Heal. 14+ years turning service centers into revenue engines using AI agents, n8n, and automation architecture.",
        "status": "published",
    },
    {
        "slug": "service-plus-ai-thesis",
        "title": "Service + AI: The New Operating System for CX",
        "type": "research",
        "content_md": """# Service + AI: The New Operating System for CX

Kailas Swami's core thesis is that customer experience in the next decade will be run by a combination of human judgment and AI systems.

## Why now
- Indian labor costs are rising.
- Customer expectations for instant responses are universal.
- Tools like n8n, Ollama, and OpenAI make automation accessible to SMBs.

## The four layers
1. **Data layer** — CRM, telephony, tickets, payments in one view.
2. **Workflow layer** — n8n orchestrates triggers across tools.
3. **Agent layer** — AI agents handle qualification, support, and follow-up.
4. **Human layer** — frontline teams supervise exceptions and build relationships.

## Typical outcomes
- 70% reduction in manual task time.
- 40-80% of Tier-1 support handled autonomously.
- 24/7 lead qualification without hiring.

## Where to start
Map your three most repetitive processes. Automate the most boring one first.
""",
        "excerpt": "Why Service + AI is the operating system for the next decade of customer experience in India.",
        "status": "published",
    },
    {
        "slug": "quick-heal-ai-playbook",
        "title": "Quick Heal: Building AI-Enabled Revenue Operations",
        "type": "case_study",
        "content_md": """# Quick Heal: Building AI-Enabled Revenue Operations

At Quick Heal, Kailas Swami leads digital revenue and is building the playbook for AI-driven retention and CX automation.

## Scope
- End-to-end customer lifecycle: service, retention, cross-sell and up-sell.
- Omnichannel + Marketing Cloud architecture.
- Telephony and IVR systems.
- Lead generation engines.
- NPS and CSAT strategy.
- CRM implementation and vendor management.

## Focus areas
- Shift from pure service to Service + AI.
- Automation-based revenue generation.
- Frontline upskilling for the AI era.

## Lessons learned
1. Start with a clear process map before buying tools.
2. Build a data layer first; AI is useless without clean data.
3. Keep humans in the loop for exceptions and relationship moments.
""",
        "excerpt": "How Quick Heal is transitioning from pure customer service to Service + AI revenue operations.",
        "status": "published",
    },
]


def seed():
    init_db()
    db = get_db_session()
    try:
        for doc in CORE_DOCUMENTS:
            existing = db.query(Document).filter(Document.slug == doc["slug"]).first()
            if existing:
                print(f"Skipping existing: {doc['slug']}")
                continue
            db.add(Document(
                id=uuid.uuid4(),
                slug=doc["slug"],
                title=doc["title"],
                type=doc["type"],
                content_md=doc["content_md"],
                excerpt=doc["excerpt"],
                status=doc["status"],
            ))
            print(f"Added: {doc['slug']}")
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
