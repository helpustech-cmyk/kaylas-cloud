# Niti Marg pipeline

Automated Hinglish explainer videos with **Niti Didi** for the Niti Marg India YouTube channel.
It's built for the Hermes VPS (KVM2, 7.8 GB RAM): no animation, only still frames and voice
stitched together by FFmpeg, one video at a time.

```
6 AM cron ─► topic (NRI every 5th) ─► official page ─► script (Ollama Cloud, Niti Didi persona)
          ─► fact check (numbers vs official page) ─► voice (ElevenLabs ► Edge-TTS)
          ─► FFmpeg: long 720p + 30s Short + 15s teaser + thumbnail
          ─► Telegram: ✅ Approve / ❌ Reject / 🔁 Re-make  (+ fact-check result, streak)
poll ─────► on approve: YouTube upload (long, Short, teaser scheduled +6h), thumbnail,
            top comment, playlist, nitimarg.in post markdown
Monday ───► trends: most-viewed topics this week ─► new topic ideas with ➕ Add buttons
```

## Commands

| Command | What it does |
|---|---|
| `python -m nitimarg run` | Daily run (topic → script → video → Telegram) |
| `python -m nitimarg run --script nitimarg/data/scripts/pm-kisan.json --no-send` | Render the sample script only |
| `python -m nitimarg run --topic pm-kisan` | Force one topic |
| `python -m nitimarg poll` | Handle Telegram taps and upload approved runs |
| `python -m nitimarg trends` | Weekly sentiment check |
| `python -m nitimarg poses` | Create placeholder poses for any missing pose files |
| `python -m nitimarg status` | Videos made, streak, last runs |

Set `NM_TTS=preview` to use an offline stand-in voice for layout checks (no API calls).

## Setup on Hermes

```bash
sudo apt-get install -y ffmpeg fonts-noto-core fonts-dejavu-core
python3 -m venv /opt/nitimarg-venv
/opt/nitimarg-venv/bin/pip install -r /opt/kaylas-cloud/nitimarg/requirements.txt
cp nitimarg/.env.example nitimarg/.env   # fill in keys; never commit .env
crontab -e                               # paste nitimarg/crontab.example
```

- **Telegram:** create a **separate** bot with @BotFather. The kaylas-cloud bot uses a webhook,
  and Telegram doesn't allow `getUpdates` polling while a webhook is set. Only taps from
  `NM_TELEGRAM_CHAT_ID` are accepted.
- **YouTube:** create an OAuth client (Desktop) in Google Cloud with YouTube Data API v3
  enabled, sign in once with the Niti Marg channel account (scope
  `https://www.googleapis.com/auth/youtube.force-ssl`), and store the refresh token in
  `NM_YT_REFRESH_TOKEN`. Custom thumbnails need a phone-verified channel. The API can't pin
  comments, so pin the top comment once in YouTube Studio (the bot reminds you).
- **Poses:** replace the placeholder files in `nitimarg/poses/` with the real art, keeping
  the same names: `<pose>_open.png` and `<pose>_closed.png`, transparent PNG, about 800×1000.
  Poses: `neutral`, `happy_pointing`, `worried`, `explaining`, `warning`, `celebrating`,
  `thinking`, `holding_phone`. Real files are never overwritten.
- **Topics** live in `data/topics.json` (set `NM_DATA_DIR` to keep them outside the git
  checkout, since the ➕ Add button edits this file).

## Files

| File | Role |
|---|---|
| `characters/niti_didi.json` | Character file: look, palette, poses, voice, persona prompt |
| `data/topics.json` | Topic queue with official source per topic |
| `data/scripts/pm-kisan.json` | Approved sample script (doc section 14) |
| `script.py` | Prompt, story structure, validation |
| `factcheck.py` | Reads the official page, flags numbers not found there |
| `tts.py`, `audio.py` | Voice, WAV helpers, loudness lip-sync |
| `render.py`, `placeholders.py` | Frames, FFmpeg encode, thumbnail, placeholder poses |
| `publish.py` | Title/description/chapters/tags/pinned comment/website post |
| `telegram.py`, `youtube.py` | Approval gate and upload |
| `pipeline.py`, `__main__.py` | Orchestration and CLI |

Tests: `python -m pytest nitimarg/tests -q`.

Not built yet: cross-posting to Instagram Reels, Facebook and WhatsApp (doc section 12), and the
two later characters (Ramu Kaka, Rahul the NRI).
