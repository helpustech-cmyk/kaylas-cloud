# Original Master Blueprint (as provided by the user, 2026-07-05)

This is the verbatim project brief the user supplied at project kickoff.
Kept here unedited for reference — see `../BLUEPRINT.md` for the living,
decision-tracked version that supersedes anything here when the two
disagree.

---

## MASTER BLUEPRINT: KAYLAS.CLOUD - THE FUTURISTIC AI DIGITAL TWIN & PERSONAL OS

### Core Mission

To build a futuristic, fully automated website acting as a Digital Revenue
Leader & AI Infrastructure Expert. It serves as a public-facing AI Brand, a
private VPS Control Tower, and a Personal Productivity OS. It features a
Matrix-style AI avatar that talks to visitors using your voice and CV data.

### Section 1: The Futuristic AI Avatar

Create an interactive AI Avatar that represents Kailas Swami — animated
digital face made of green matrix coding lines against a flashy black,
neon-lit background. Three.js or CSS/JS canvas for matrix rain. Wav2Lip or
CSS/JS lip-sync library for lip movement. ElevenLabs or Web Speech API for
voice. RAG knowledge base (Pinecone/ChromaDB) fed with resume, skills,
research papers, blogs — retrieves answers, speaks them, syncs lips.

### Section 2: Revised Professional Bio & Skillset

Current Role: Digital Revenue Lead at Quack Heal (Customer Lifecycle,
Service & Retention, Cross-sale & Up-sale). Core Expertise: Communication
Channel Expert, Marketing Cloud & Service Tools Expert, Telephony Expert,
Lead Generation Expert, Customer Communication Expert. Strategic Metrics:
NPS & CSAT Expert, Customer Personalization Guru, Retention & Revenue
Generator. Operational Leadership: Vendor Management, Vendor Hiring,
Process Optimization, CRM Implementation. Future Tech Stack: AI Process
Engineering, AI/ML for CX, Customer Psychology, Digital Transformation 4.0.
"New World" Skill Set: Service + AI, automation-driven revenue, upskilling
frontline staff for the AI era.

### Section 3: "WOW" UX Hacks

System-initialization boot loading screen. 3D parallax depth on mouse move.
Glitchy scrolling chat text. Click ripple effects. Futuristic glowing
cursor.

### Section 4: Phase-by-Phase Development

- **Phase 1** — VPS recon (SSH into Hostinger VPS, OS/Docker/ports check,
  install Docker if missing, verify DNS).
- **Phase 2** — AI Avatar & Knowledge Base: ChromaDB on VPS, embed CV +
  skillset + research papers, middleware API (query → retrieve → TTS →
  lip-sync).
- **Phase 3** — Frontend 20/20/60 layout: top nav, left contact panel,
  main dynamic tab container, floating avatar chat widget.
- **Phase 4** — 7 public tabs: Resume, Research Lab & YouTube, AI Knowledge
  Hub, Automation Repos, Service Leaders Training, Social Media Wall, Admin
  Control Tower.
- **Phase 5** — Lead-gen modal → WhatsApp Business API/Twilio webhook on
  submit; Google Calendar booking → second WhatsApp notification; reveal
  blurred contact info on submit.
- **Phase 6** — Hostinger affiliate link integration + click/lead tracking
  dashboard in Admin tab.
- **Phase 7** — Personal Productivity OS in Admin Panel: POA generator
  (LLM-drafted plans), OKR/goal tracker with progress bars, weekly PDF
  report export, smart WhatsApp/Telegram deadline reminders via cron.
- **Phase 8** — Research paper learning loop: upload PDF → AI summary + 10Q
  comprehension test → 80%+ pass unlocks "Approve & Publish" → n8n
  auto-publishes to Knowledge Hub, YouTube, LinkedIn, Twitter, Telegram,
  WhatsApp Broadcast.
- **Phase 9** — VPS Control Tower in Admin Panel: browser SSH terminal
  (ttyd or custom), n8n UI launcher, Hermes Docker UI launcher, FileBrowser
  container for file editing without FTP.

### Section 5: Pre-Execution Checklist

VPS IP + SSH root password; existing containers on port 80/443; preferred
DB for OKR tracker; ElevenLabs vs free Web Speech API; API keys ready for
WhatsApp Business, YouTube, LinkedIn, Twitter.

### Final Directive

Execute Phase 1 immediately after VPS details are provided. Follow phases
in strict order — don't start Phase 3 until Phase 2 is fully functional.
Build as commercial-grade, self-healing AI infrastructure.

---

**Deviation logged in `../BLUEPRINT.md`**: root SSH passwords are not
requested or accepted in chat, for security reasons — SSH key exchange is
used instead. This is the only deliberate departure from the brief above.
