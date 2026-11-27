"""Daily run, approval polling and the weekly trend check."""

from __future__ import annotations

import json
import logging
import shutil
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from . import factcheck, publish, render, state, telegram, topics, tts, youtube
from .config import Config
from .placeholders import ensure_poses
from .script import generate_script, save_script, slugify

log = logging.getLogger(__name__)


def _notify(cfg: Config, text: str) -> None:
    if telegram.enabled(cfg):
        try:
            telegram.send_text(cfg, text)
        except Exception as exc:
            log.error("Telegram notify failed: %s", exc)


def make_videos(cfg: Config, script: dict[str, Any], run_dir: Path) -> dict[str, Any]:
    """Voice + long video + Short + teaser + thumbnail for one script."""
    ensure_poses(cfg.poses_dir)
    voice_dir = run_dir / "voice"
    wavs: dict[str, Path] = {}
    engines = set()
    for b in script["beats"]:
        wavs[b["beat"]] = voice_dir / f"{b['beat']}.wav"
        engines.add(tts.speak(cfg, b["line"], wavs[b["beat"]]))

    # Shorter lines for the Short when the script provides them
    short_wavs = dict(wavs)
    short_script = json.loads(json.dumps(script))
    for name, line in script.get("short", {}).items():
        short_wavs[name] = voice_dir / f"short_{name}.wav"
        engines.add(tts.speak(cfg, line, short_wavs[name]))
        for b in short_script["beats"]:
            if b["beat"] == name:
                b["line"] = line

    long = render.render(cfg, script, wavs, run_dir / "long.mp4", cfg.long_size)
    short = render.render(cfg, short_script, short_wavs, run_dir / "short.mp4", cfg.short_size,
                          beats=script["short_beats"], intro=False, endcard=True,
                          max_seconds=cfg.short_max_seconds)
    teaser = render.render(cfg, short_script, short_wavs, run_dir / "teaser.mp4", cfg.short_size,
                           beats=["hook"], intro=False, endcard=True, max_seconds=cfg.teaser_max_seconds)
    thumb = render.thumbnail(cfg, script, run_dir / "thumbnail.jpg")
    for d in run_dir.glob("*_frames"):  # frames are cheap to rebuild; keep disk small
        shutil.rmtree(d, ignore_errors=True)
    return {"long": long, "short": short, "teaser": teaser, "thumbnail": str(thumb),
            "voice": sorted(engines)}


def run_daily(cfg: Config, topic_id: str | None = None, script_file: Path | None = None,
              send: bool = True) -> dict[str, Any]:
    """Pick a topic, write and check the script, render, send for approval."""
    cfg.work_dir.mkdir(parents=True, exist_ok=True)
    with state.single_instance(cfg.work_dir / "render.lock"):
        st = state.load(cfg.state_file)
        all_topics = topics.load_topics(cfg.topics_file)
        if script_file:
            script = json.loads(script_file.read_text(encoding="utf-8"))
            topic = next((t for t in all_topics if t["id"] == script.get("topic_id")),
                         {"id": script.get("topic_id", "manual"), "name": script.get("topic_name", ""),
                          "official_url": script.get("source_url", "")})
        else:
            topic = (next(t for t in all_topics if t["id"] == topic_id) if topic_id
                     else topics.pick_topic(all_topics, st["used_topics"], st["videos_made"], cfg.nri_every))
            script = None

        try:
            source_text = factcheck.fetch_source(topic["official_url"])
        except Exception as exc:
            log.warning("Could not read %s: %s", topic["official_url"], exc)
            source_text = ""
        if script is None:
            script = generate_script(cfg, topic, source_text)
        report = factcheck.check(script, source_text)
        if cfg.factcheck_strict and not report["ok"]:
            _notify(cfg, f"⛔ Niti Marg: script for {topic['name']} failed the fact check.\n"
                         + factcheck.summary(report))
            raise RuntimeError("Fact check failed: " + ", ".join(report["missing"]))

        run_id = datetime.now().strftime("%Y%m%d-%H%M") + "-" + slugify(topic["id"])[:20]
        run_dir = cfg.work_dir / "runs" / run_id
        save_script(script, run_dir / "script.json")
        videos = make_videos(cfg, script, run_dir)
        desc = publish.description(script, videos["long"]["chapters"], videos["long"]["duration"],
                                   cfg.website)
        (run_dir / "description.txt").write_text(desc, encoding="utf-8")
        (run_dir / "post.md").write_text(publish.website_post(script, None), encoding="utf-8")

        run = {"id": run_id, "topic_id": topic["id"], "dir": str(run_dir), "status": "pending",
               "created": datetime.now().isoformat(timespec="seconds"), "factcheck": report,
               "videos": videos}
        st["runs"][run_id] = run
        if topic["id"] not in st["used_topics"]:
            st["used_topics"].append(topic["id"])
        st["videos_made"] += 1
        state.save(cfg.state_file, st)

        if send and telegram.enabled(cfg):
            send_for_approval(cfg, run, script, st)
        return run


def send_for_approval(cfg: Config, run: dict[str, Any], script: dict[str, Any], st: dict[str, Any]) -> None:
    run_dir = Path(run["dir"])
    streak = state.streak(st["approved_days"])
    caption = "\n".join([
        f"🎬 Niti Marg: {script['title']}",
        f"⏱ {publish.fmt_ts(run['videos']['long']['duration'])} | voice: {', '.join(run['videos']['voice'])}",
        factcheck.summary(run["factcheck"]),
        f"🔗 {script['source_url']}",
        f"🔥 Streak: {streak} day{'s' if streak != 1 else ''}",
    ])
    telegram.send_video(cfg, run_dir / "long.mp4", caption, telegram.approval_buttons(run["id"]))
    telegram.send_video(cfg, run_dir / "short.mp4", "📱 Short (uploads with the main video)")
    telegram.send_video(cfg, run_dir / "teaser.mp4",
                        f"⏳ 15s teaser (goes live {cfg.teaser_delay_hours}h after upload)")


def upload_run(cfg: Config, run: dict[str, Any]) -> dict[str, Any]:
    run_dir = Path(run["dir"])
    script = json.loads((run_dir / "script.json").read_text(encoding="utf-8"))
    desc = (run_dir / "description.txt").read_text(encoding="utf-8")
    token = youtube.access_token(cfg)
    tags = publish.tags(script)
    result: dict[str, Any] = {"notes": []}

    vid = youtube.upload_video(cfg, token, run_dir / "long.mp4", script["title"], desc, tags)
    result["long"] = vid
    long_url = f"https://youtu.be/{vid}"
    for label, fn in (
        ("thumbnail", lambda: youtube.set_thumbnail(token, vid, run_dir / "thumbnail.jpg")),
        ("comment", lambda: youtube.add_comment(token, vid, publish.pinned_comment(script))),
        ("playlist", lambda: youtube.add_to_playlist(token, youtube.playlist_id(token, script["playlist"]), vid)
         if script.get("playlist") else None),
    ):
        try:
            fn()
        except Exception as exc:
            result["notes"].append(f"{label}: {exc}")

    short_desc = publish.short_description(script, long_url)
    result["short"] = youtube.upload_video(cfg, token, run_dir / "short.mp4", publish.short_title(script),
                                           short_desc, tags)
    publish_at = datetime.now(timezone.utc) + timedelta(hours=cfg.teaser_delay_hours)
    result["teaser"] = youtube.upload_video(cfg, token, run_dir / "teaser.mp4",
                                            publish.short_title(script), short_desc, tags,
                                            publish_at=publish_at)
    (run_dir / "post.md").write_text(publish.website_post(script, vid), encoding="utf-8")
    return result


def poll_approvals(cfg: Config) -> int:
    """Handle Approve / Reject / Re-make taps. Run every few minutes from cron."""
    if not telegram.enabled(cfg):
        raise RuntimeError("Telegram is not configured (NM_TELEGRAM_BOT_TOKEN / NM_TELEGRAM_CHAT_ID)")
    st = state.load(cfg.state_file)
    handled = 0
    for upd in telegram.get_updates(cfg, st["tg_offset"]):
        st["tg_offset"] = upd["update_id"] + 1
        parsed = telegram.parse_callback(upd)
        if not parsed:
            continue
        cb_id, action, run_id, chat_id = parsed
        if chat_id != str(cfg.telegram_chat_id):  # only Kaylas can approve
            continue
        if action == "topic":
            telegram.answer(cfg, cb_id, enable_topic(cfg, run_id))
            handled += 1
            continue
        run = st["runs"].get(run_id)
        if not run or run["status"] != "pending":
            telegram.answer(cfg, cb_id, "Already handled")
            continue
        handled += 1
        if action == "approve":
            telegram.answer(cfg, cb_id, "Uploading…")
            run["status"] = "uploading"
            state.save(cfg.state_file, st)
            try:
                res = upload_run(cfg, run)
                run.update(status="uploaded", youtube=res)
                today = date.today().isoformat()
                if today not in st["approved_days"]:
                    st["approved_days"].append(today)
                notes = ("\n⚠️ " + "\n⚠️ ".join(res["notes"])) if res["notes"] else ""
                telegram.send_text(cfg, f"✅ Live: https://youtu.be/{res['long']}\n"
                                        f"📱 Short: https://youtu.be/{res['short']}\n"
                                        f"📌 Pin the top comment in YouTube Studio.{notes}\n"
                                        f"🔥 Streak: {state.streak(st['approved_days'])} days")
            except Exception as exc:
                run["status"] = "pending"
                telegram.send_text(cfg, f"⛔ Upload failed for {run_id}: {exc}")
        elif action == "reject":
            run["status"] = "rejected"
            telegram.answer(cfg, cb_id, "Rejected")
        elif action == "redo":
            run["status"] = "redo"
            st["used_topics"] = [t for t in st["used_topics"] if t != run["topic_id"]]
            telegram.answer(cfg, cb_id, "Will re-make at the next run")
        state.save(cfg.state_file, st)
    state.save(cfg.state_file, st)
    return handled


TREND_QUERIES = ["sarkari yojana", "new rule change money", "scheme last date", "NRI tax India",
                 "loan scheme government", "scam alert UPI"]


def weekly_trends(cfg: Config) -> list[dict[str, Any]]:
    """Find what people worry about this week and propose new topics on Telegram."""
    from .llm import chat_json

    token = youtube.access_token(cfg)
    titles = youtube.trending_titles(token, TREND_QUERIES)
    all_topics = topics.load_topics(cfg.topics_file)
    known = ", ".join(t["name"] for t in all_topics)
    reply = chat_json(cfg, "You pick Indian money and government scheme topics for a Hinglish explainer channel.",
                      f"""Popular video titles this week:
{chr(10).join('- ' + t for t in titles[:60])}

Already covered: {known}

Propose up to 5 NEW topics people are worried about (rule changes, deadlines, scams, benefits).
Each must have an official government source page. JSON:
{{"topics": [{{"id": "kebab-id", "name": "...", "category": "kisan|women|loans|nri|pm-tenure|general",
"official_url": "https://....gov.in/...", "keywords": ["..."], "why": "one line"}}]}}""")
    proposed = []
    ids = {t["id"] for t in all_topics}
    for t in reply.get("topics", [])[:5]:
        if not t.get("id") or t["id"] in ids or ".gov.in" not in str(t.get("official_url", "")) \
                and ".nic.in" not in str(t.get("official_url", "")):
            continue
        t = {k: t[k] for k in ("id", "name", "category", "official_url", "keywords") if k in t} | {
            "enabled": False, "priority": 1, "proposed": date.today().isoformat(), "why": t.get("why", "")}
        all_topics.append(t)
        proposed.append(t)
    topics.save_topics(cfg.topics_file, all_topics)
    if proposed and telegram.enabled(cfg):
        for t in proposed:
            telegram.send_text(cfg, f"🆕 Topic idea: {t['name']}\n{t.get('why', '')}\n{t['official_url']}",
                               [[{"text": "➕ Add to queue", "callback_data": f"nm:topic:{t['id']}"}]])
    return proposed


def enable_topic(cfg: Config, topic_id: str) -> str:
    all_topics = topics.load_topics(cfg.topics_file)
    for t in all_topics:
        if t["id"] == topic_id:
            t["enabled"] = True
            topics.save_topics(cfg.topics_file, all_topics)
            return f"Added: {t['name']}"
    return "Topic not found"
