# Kaylas.cloud — Project Blueprint & Status

This file is the single source of truth for this project. Any AI assistant
(Claude, Freebuff AI, or otherwise) picking up this repo should read this
file first, then check `git log` for what actually changed and when.
Do not deviate from decisions already locked in below without the user's
explicit sign-off — if a change seems necessary, propose it and update this
file in the same commit.

## Mission

A futuristic personal site for Kailas Swami: an AI avatar (matrix-rain
aesthetic) that answers visitor questions about his CV/expertise using a
retrieval + TTS pipeline, plus (later phases) a VPS control tower, lead-gen
automation, and a personal productivity OS. Full original spec from the user
is preserved in `docs/ORIGINAL_BLUEPRINT.md`.

## Locked decisions (do not re-litigate without asking the user)

- **Stack**: Vite + React + TypeScript, no framework lock-in beyond that yet.
- **Access to the VPS**: SSH key-based only. Never request or paste root
  passwords in chat/session text.
- **Starting point**: local scaffold first, deploy to the real Hostinger VPS
  only once the avatar + chat MVP works locally.
- **Codebase**: fresh repo at `/root/kaylas-cloud` (this directory).
- **Current role/employer**: Digital Revenue Lead at **Quick Heal** (not
  "Quack Heal" — that spelling in the original brief was a typo), since
  September 2025. Prior role was Head Customer Service at Parag Milk Foods
  Limited (Dec 2024–Sept 2025). Full career history in `docs/CV_SOURCE.md`.
- **TTS (current phase)**: Web Speech API (free, browser-native). ElevenLabs
  is a planned upgrade once the user sets up a paid account — swap happens
  inside `src/hooks/useSpeech.ts` only.
- **Knowledge base (current phase)**: local keyword-retrieval over
  `src/data/knowledge.ts` (see `src/lib/retrieval.ts`). This is a deliberate
  stand-in for the real RAG/vector-DB pipeline (Pinecone/ChromaDB + OpenAI
  embeddings) described in the original blueprint's Phase 2 — swap the
  `answer()` function signature stays the same so callers don't change.

## Phase status

| Phase | Description | Status |
|---|---|---|
| 0 | Local MVP scaffold: matrix rain, AI avatar (SVG, lip-sync via speech boundary events), chat console, local retrieval, Web Speech TTS | ✅ Done — verified in headless browser, no console errors |
| 1 | VPS recon (SSH, Docker, DNS check) | Not started — detailed plan in `docs/PHASE1_VPS_BLUEPRINT.md`; needs user to provide VPS host/port/username and SSH public key setup |
| 2 | Real RAG: vector DB (ChromaDB) + OpenAI embeddings | Not started — real CV content is now in the knowledge base (keyword retrieval), still needs an OpenAI API key to upgrade to embeddings |
| 3 | Full 20/20/60 layout polish, 3D parallax, loading screen, cursor/ripple effects | Partial — tab navigation + floating avatar widget done, no parallax/loader/cursor yet |
| 4 | 7 public tabs (Resume, Research, Knowledge Hub, Repos, Training, Social Wall, Admin) | Partial — tab switching works; Resume tab has real CV content (accordion of jobs, education, certifications, achievements, skills); Research/Knowledge/Repos/Training/Social are styled placeholders; Admin not started |
| 5 | Lead-gen modal + WhatsApp/Calendar automation | Not started — needs WhatsApp Business API / Twilio + Google Calendar API keys |
| 6 | Hostinger affiliate tracking | Not started |
| 7 | Admin productivity OS (POA generator, OKR tracker, reports, reminders) | Not started — needs DB choice confirmed and an LLM API key |
| 8 | Research-paper approval + auto-publish workflow (n8n) | Not started — needs n8n on the VPS plus social API keys |
| 9 | VPS control tower (in-browser terminal, file manager, n8n/Hermes links) | Not started — needs VPS access |

## What exists right now

```
kaylas-cloud/
  src/
    components/MatrixRain.tsx    — canvas matrix rain background
    components/AIAvatar.tsx      — SVG face, mouth driven by mouthLevel prop
    components/ChatConsole.tsx   — chat log + input, calls retrieval + TTS
    hooks/useSpeech.ts           — Web Speech API wrapper, exposes isSpeaking/mouthLevel
    lib/retrieval.ts             — keyword-overlap answer(query) over knowledge.ts
    data/knowledge.ts            — knowledge base (real CV content, see docs/CV_SOURCE.md)
    data/resume.ts               — structured CV data feeding the Resume tab UI
    components/tabs/             — ResumeTab (real content) + PlaceholderTab (Research/Knowledge/Repos/Training/Social)
    components/FloatingAvatarWidget.tsx — bottom-right persistent chat widget
    App.tsx / App.css            — layout + neon/matrix styling
```

Run locally: `npm install && npm run dev` (Vite, default port 5173).

## Immediate next step (as of 2026-07-05)

Deployed. User ran `npx vercel login` in their own terminal (Vercel account:
`helpustech-1561`). Project linked as `helpustech/kaylas-cloud` and deployed
at commit `121db01`. Live URL: **https://kaylas-cloud.vercel.app** (Vercel
auto-aliased this as the project's first deployment — it's still just the
free Vercel domain, not the real `kaylas.cloud` domain). Next: user reviews
the live site, then decide on kaylas.cloud DNS cutover (separate later step)
and/or continue with Phase 1 (VPS recon) once ready.

## Open questions blocking later phases

- ~~Real CV/resume PDF content~~ — done, see `docs/CV_SOURCE.md` and
  `src/data/knowledge.ts`
- OpenAI API key (embeddings) — only needed for Phase 2
- ElevenLabs account — only needed to upgrade TTS quality
- WhatsApp Business/Twilio, YouTube, LinkedIn, Twitter/X API keys — only
  needed for Phase 5/8
- Preferred DB for the OKR/goal tracker (Postgres/MySQL/SQLite) — only
  needed for Phase 7
- VPS SSH public key exchange — only needed for Phase 1 onward

## Continuity note

Every meaningful change should land as a git commit with a message
explaining *why*, not just *what* — `git log` is the audit trail. Keep this
file's phase table and "locked decisions" section updated in the same
commit as any structural change, so the project stays coherent no matter
which AI assistant or session continues the work.
