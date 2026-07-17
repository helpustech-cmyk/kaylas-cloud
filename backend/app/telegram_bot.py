"""Telegram webhook handler for @Helpustech_bot"""
import os
import json
import logging
from typing import Optional
from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Request, HTTPException

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

router = APIRouter()

TOPICS = [
    {"id": 1, "bucket": "Operational Pain Points", "title": "Why your support team costs more than it should", "lesson": "Most Indian companies spend 60-70% of support budget on Level 1 queries that could be automated. The fix: map every query type, measure handle time, and build a triage bot for the top 20% query types."},
    {"id": 2, "bucket": "Operational Pain Points", "title": "The real cost of manual renewals", "lesson": "Every manual renewal follow-up costs ~₹200-500 in agent time. At 10,000 renewals/month, that's ₹20-50L. Automated reminder sequences + payment links cut this by 80%."},
    {"id": 3, "bucket": "Where AI Breaks", "title": "Why AI bots hallucinate — and how to catch it", "lesson": "LLMs don't 'know' facts — they predict the next word. Hallucination happens when the model fills gaps with plausible-sounding fiction. Fix: always ground responses in retrieved documents (RAG), never let the model answer from memory alone."},
    {"id": 4, "bucket": "Human Side of AI", "title": "Your team will resist automation. Here's why.", "lesson": "People don't resist automation — they resist being replaced without a plan. The winning pattern: automate the boring parts first, then upskill the team to handle exceptions and strategy. Show them the roadmap, don't hide it."},
    {"id": 5, "bucket": "Craft of Building Systems", "title": "The one automation rule you must never break", "lesson": "Never automate a broken process. If the manual flow has errors, automation just makes errors faster. Fix the process first, measure it, then automate. Garbage in = garbage out, at machine speed."},
    {"id": 6, "bucket": "Business Case & Leadership", "title": "How to calculate ROI on an AI bot", "lesson": "ROI = (Cost saved - Build cost) / Build cost × 100. Cost saved = (Avg handle time × Volume × Agent cost) - (Bot cost per query × Volume). A bot that costs ₹5L to build and saves ₹2L/month pays for itself in 2.5 months."},
]

TOPIC_INDEX = 0  # Will be persisted via API


async def send_telegram_message(text: str, parse_mode: str = "Markdown") -> Optional[dict]:
    if not TELEGRAM_BOT_TOKEN:
        return None
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": parse_mode}
    async with httpx.AsyncClient(timeout=20.0) as client:
        res = await client.post(url, json=payload)
        res.raise_for_status()
        return res.json()


async def send_telegram_buttons(text: str, buttons: list[list[dict]]) -> Optional[dict]:
    if not TELEGRAM_BOT_TOKEN:
        return None
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": {"inline_keyboard": buttons},
    }
    async with httpx.AsyncClient(timeout=20.0) as client:
        res = await client.post(url, json=payload)
        res.raise_for_status()
        return res.json()


@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    """Receive updates from Telegram bot"""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Handle callback queries (button clicks)
    if "callback_query" in body:
        cb = body["callback_query"]
        data = cb.get("data", "")
        msg = cb.get("message", {})
        chat_id = msg.get("chat", {}).get("id")
        message_id = msg.get("message_id")

        if data == "learned_yes":
            await send_telegram_message(
                f"✅ *Topic marked complete!*\n\nGenerating blog post, research note, and video script from our conversation...\n\n⏳ Ready in ~2 minutes.",
                parse_mode="Markdown"
            )
            # Acknowledge the callback
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
            async with httpx.AsyncClient() as client:
                await client.post(url, json={"callback_query_id": cb["id"], "text": "✅ Marked as learned!"})
            return {"ok": True}

        elif data == "learned_no":
            await send_telegram_message(
                "No problem! Take your time. Reply with your questions or say *LEARNED* when you're ready.",
                parse_mode="Markdown"
            )
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
            async with httpx.AsyncClient() as client:
                await client.post(url, json={"callback_query_id": cb["id"], "text": "Take your time!"})
            return {"ok": True}

        elif data.startswith("content_"):
            action = data.replace("content_", "")
            if action == "approve":
                await send_telegram_message("✅ *Approved!* Queued for publishing tomorrow at 9 AM IST.")
            elif action == "edit":
                await send_telegram_message("✏️ Send me the edits you want, or type *approve* to publish as-is.")
            elif action == "reject":
                await send_telegram_message("❌ Rejected. Moving to next topic.")
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
            async with httpx.AsyncClient() as client:
                await client.post(url, json={"callback_query_id": cb["id"]})
            return {"ok": True}

        return {"ok": True}

    global TOPIC_INDEX

    # Handle regular messages
    if "message" in body:
        msg = body["message"]
        text = msg.get("text", "").strip()
        chat_id = msg.get("chat", {}).get("id")

        # Only respond to our chat
        if str(chat_id) != TELEGRAM_CHAT_ID:
            return {"ok": True}

        lower = text.lower()

        if lower == "/start":
            await send_telegram_message(
                "*👋 Welcome to your Learning Bot!*\n\nI'm your daily mentor. Every morning I'll send you a topic to learn. Reply with questions, then say *LEARNED* when done.\n\nType */topic* for today's lesson\nType */next* to skip to next topic\nType */status* to see your progress"
            )

        elif lower == "/topic" or lower == "/next":
            if TOPIC_INDEX >= len(TOPICS):
                await send_telegram_message("🎉 *All topics complete!* You've finished the entire curriculum. New topics coming soon.")
                return {"ok": True}
            t = TOPICS[TOPIC_INDEX]
            msg_text = (
                f"*📚 Topic {TOPIC_INDEX + 1}/{len(TOPICS)} — {t['bucket']}*\n\n"
                f"*{t['title']}*\n\n"
                f"{t['lesson']}\n\n"
                f"Ask me anything about this topic. When you're done, tap *LEARNED* below."
            )
            buttons = [[
                {"text": "✅ LEARNED", "callback_data": "learned_yes"},
                {"text": "❌ Not yet", "callback_data": "learned_no"},
            ]]
            await send_telegram_buttons(msg_text, buttons)

        elif lower == "/status":
            done = TOPIC_INDEX
            total = len(TOPICS)
            bar = "█" * done + "░" * (total - done)
            await send_telegram_message(
                f"*📊 Progress*\n\n`{bar}`\n\n{done}/{total} topics completed ({round(done/total*100)}%)\n\nKeep going! 🚀"
            )

        elif lower == "learned":
            if TOPIC_INDEX < len(TOPICS):
                t = TOPICS[TOPIC_INDEX]
                TOPIC_INDEX += 1
                await send_telegram_message(
                    f"✅ *{t['title']}* — marked complete!\n\n"
                    f"Generating blog post, research note, and video script...\n\n"
                    f"⏳ Ready in ~2 minutes."
                )
            else:
                await send_telegram_message("🎉 All topics done!")

        elif lower in ["hello", "hi", "hey"]:
            await send_telegram_message("Hey! Ready to learn? Type */topic* to start today's lesson.")

        else:
            # Any other message — treat as a question about the current topic
            await send_telegram_message(
                f"Good question! Think about it in context of the current topic. When you feel you've understood, type *LEARNED* to mark it complete and move on."
            )

    return {"ok": True}


@router.post("/telegram/send-topic")
async def send_daily_topic():
    """Endpoint called by cron/n8n to push the daily topic"""
    if TOPIC_INDEX >= len(TOPICS):
        return {"status": "all_done", "topics_completed": len(TOPICS)}

    t = TOPICS[TOPIC_INDEX]
    msg_text = (
        f"*📚 Daily Topic — {t['bucket']}*\n\n"
        f"*{t['title']}*\n\n"
        f"{t['lesson']}\n\n"
        f"Ask questions, then tap *LEARNED* when done."
    )
    buttons = [[
        {"text": "✅ LEARNED", "callback_data": "learned_yes"},
        {"text": "❌ Not yet", "callback_data": "learned_no"},
    ]]
    await send_telegram_buttons(msg_text, buttons)
    return {"status": "sent", "topic": t["title"], "topic_index": TOPIC_INDEX}


@router.get("/telegram/topics")
async def list_topics():
    """List all topics and current progress"""
    return {
        "total": len(TOPICS),
        "current_index": TOPIC_INDEX,
        "current_topic": TOPICS[TOPIC_INDEX]["title"] if TOPIC_INDEX < len(TOPICS) else None,
        "topics": TOPICS,
    }
