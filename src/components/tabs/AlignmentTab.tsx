import { useState, useEffect } from 'react'

const ARTICLES = [
  {
    id: 'the-great-divide',
    title: 'The Great Divide: Why Ops, Product, and Tech Build Different Bots',
    summary: 'The single biggest reason service bots fail has nothing to do with technology. It is the gap between what operations teams need, what product teams spec, and what engineering teams build.',
    readTime: '6 min',
    content: `Every service bot I have seen fail — and I have seen enough to fill a graveyard — failed for the same reason. Not because the NLP model was weak. Not because the latency was too high. Not because the vendor was bad.

They failed because three teams built three different bots.

**The Operations Team** wanted a bot that reduces agent workload. They imagined a system that handles the repetitive queries — password resets, billing inquiries, order status — so their agents can focus on complex issues. They wanted it in 4 weeks. They wanted it to work on chat and WhatsApp. They wanted it to cost less than Rs 5L.

**The Product Team** wanted a bot that delights customers. They wrote user stories about "seamless experiences" and "conversational AI." They wanted it to handle every query type. They wanted it to feel human. They wanted it to be ready for the board meeting in 3 months.

**The Engineering Team** wanted to build it right. They talked about fine-tuning BERT models, vector databases, Kubernetes auto-scaling, and custom CRM integrations. They said it would take 4 months and cost Rs 25L.

Three teams. Three timelines. Three budgets. Three definitions of success.

And the bot? It launched in week 8 with 20 KB articles, keyword matching that missed 40% of intents, and no escalation path. It handled 23 queries correctly before the team pulled the plug.

**The Rs 18L lesson:** Alignment is not a nice-to-have. It is the difference between a bot that works and a bot that wastes everyone's time.

### How Alignment Breaks

The gap opens in three places:

**1. Language.** Ops says "query type." Tech says "intent." Product says "user story." Same concept, three different words. The team spends weeks debating terminology instead of building.

**2. Timeline.** Ops needs it in 4 weeks. Tech needs 16 weeks. Product compromises on 8 weeks. Everyone knows 8 weeks is not enough. Nobody says it. The bot launches broken.

**3. Success metrics.** Ops measures CSAT and handle time. Tech measures uptime and latency. Product measures feature adoption. When the bot has 99.9% uptime but 40% CSAT, tech calls it a success and ops calls it a failure.

### The Fix

Before writing a single line of code, three teams must agree on one document:

- **What the bot CAN do** (list of intents, confidence thresholds, channels)
- **What the bot CANNOT do** (query types that always escalate, known limitations)
- **Escalation rules** (when to hand off, where to hand off, what context to pass)
- **Maintenance schedule** (who reviews the KB every Monday)
- **Rollback plan** (if resolution drops below 50%, the bot is paused)

This document is not a PRD. It is not a technical spec. It is a **handoff agreement** between three teams that usually do not talk to each other.

The best bot I ever built was not the one with the most sophisticated model. It was the one where ops, product, and tech sat in the same room, spoke the same language, and agreed on what success looked like.

Build the bot together. Or do not build it at all.`
  },
  {
    id: 'voice-channel',
    title: 'Voice: The Hardest Channel. The Highest Impact.',
    summary: 'Every vendor will tell you voice is "just another channel." It is not. Voice is where your bot\'s 200ms latency becomes audible, where Indian accents break STT engines, and where customers expect a human and hear a machine.',
    readTime: '5 min',
    content: `Voice is the channel where the customer can hear your bot think. Two hundred milliseconds of silence between words feels like an eternity when you are on a call. Background noise — traffic, TV, kids, kitchen — destroys speech-to-text accuracy. Indian accents, code-switching, and regional dialects break every STT engine differently.

And the customer? They called because they wanted to talk to a human. When they hear a bot, the trust deficit starts at hello.

### What You Actually Need

A voice bot is not "just another integration." It requires:

- **A telephony provider** (Exotel, Knowlarity, Twilio, Plivo)
- **STT engine** (speech-to-text — Google, Azure, Deepgram, AssemblyAI)
- **TTS engine** (text-to-speech — Google, Azure, ElevenLabs)
- **Warm transfer** — when the bot escalates, the human agent must see full context. No "I already told the bot everything" frustration.
- **Call recording storage** — for compliance and training

### The Ops-Product-Tech Gap in Voice

**Ops** wants the bot to reduce call volume. They measure calls handled, handle time, abandonment rate.

**Product** wants the bot to sound human. They write scripts that sound natural but are impossible to implement within latency constraints.

**Tech** knows that STT + intent detection + KB lookup + TTS = minimum 1.2 seconds of latency. They also know that Indian English STT is 10-15% less accurate than US English.

The gap: Ops expects 80% resolution. Tech delivers 60%. Product is unhappy with the voice quality. The bot gets blamed.

### The Ground Truth

Start with chat. Prove the concept. Then move to voice. Anyone who tells you to start with voice has not deployed one.`
  },
  {
    id: 'web-chat',
    title: 'Web Chat: The Easiest Channel. The Easiest to Get Wrong.',
    summary: 'Chat should be the easiest channel. No STT errors. No TTS latency. The customer types, the bot reads, the bot responds. And yet most chat bots fail — because the design is wrong, not the technology.',
    readTime: '5 min',
    content: `Chat is the channel where customers have the least patience. They are already on your website. They could leave at any moment. Every second the bot wastes is a second closer to the customer closing the tab and calling your competitor.

### What Most Chat Bots Get Wrong

**They ask four questions at once.** "Please provide your name, email, order number, and reason for contact." The customer is overwhelmed. They leave.

**They ignore what the customer already said.** The customer types "I already tried that." The bot suggests the same steps again. The customer feels unheard. They get angry.

**They do not know when to shut up.** The bot gives a 500-word answer to a yes/no question. The customer does not read it. They type "???" and the bot starts over.

**They hide the "talk to agent" button.** The customer wants a human. The bot tries to convince them otherwise. The customer leaves frustrated.

### The Fix

- Show capabilities upfront: "I can help with password resets, billing, or orders."
- One field at a time. Max three fields before answering.
- Keep responses under three lines.
- "Talk to agent" button visible in every single message.
- If the customer says "already tried," pivot immediately. Do not repeat steps.
- Max five exchanges. After that, escalate.

Chat is the easiest channel to get right. It is also the easiest to get wrong. The difference is respect for the customer's time.`
  },
  {
    id: 'email-channel',
    title: 'Email: Where Bot Mistakes Live Forever',
    summary: 'A wrong answer in chat disappears when the window closes. A wrong answer in email sits in the customer\'s inbox — forwardable, screenshotable, and citable. Email mistakes have a longer shelf life than any other channel.',
    readTime: '5 min',
    content: `Email is the most deceptive channel. It looks easy. Customer writes an email. Bot reads it. Bot responds. Done.

Except email is where customers write essays. They include their life story, three unrelated problems, a screenshot that did not attach, and a complaint about something that happened six months ago — all in one email. And they expect a perfect response that addresses every single point.

### The Ops-Product-Tech Gap in Email

**Ops** wants every email answered within 4 hours. They measure SLA compliance and CSAT.

**Product** wants personalized, human-sounding responses. They want the bot to understand context, tone, and multiple intents.

**Tech** knows that email parsing is hard. A 500-word email with three intents, emotional language, and a missing attachment is a nightmare for keyword matching. LLMs handle it better, but they cost more and can hallucinate.

### The Ground Truth

Auto-send only for the safest responses — password resets and order status. Everything else needs a human to press "Send." A bot draft plus human review catches 90% of errors before they reach the customer.

Email is where bot mistakes live forever. Treat it with the respect it deserves.`
  },
  {
    id: 'sms-channel',
    title: 'SMS: 160 Characters. No Formatting. Maximum Impact.',
    summary: 'SMS reaches everyone. Not everyone has WhatsApp. Not everyone has a smartphone. But everyone with a phone receives SMS. In India, that is 1.2 billion people. The catch? You have 160 characters to communicate everything.',
    readTime: '4 min',
    content: `SMS is the most constrained channel. One hundred and sixty characters per message. No formatting. No buttons. No images. No typing indicators. No read receipts.

It is also the most underestimated.

### What SMS Is Good For

SMS is not a conversation channel. It is a notification and action channel. Use it for:

- Order confirmations and shipping updates
- Payment reminders
- OTPs and verifications
- Appointment reminders
- One-click actions ("Reply 1 for status, 2 for bill")

### What SMS Is Terrible For

- Multi-turn conversations
- Complex problem solving
- Emotional support
- Any query that needs more than 160 characters to answer

### The Ops-Product-Tech Gap in SMS

**Ops** wants to use SMS for everything because it has 98% open rates.

**Product** wants rich, interactive SMS experiences with buttons and images.

**Tech** knows that SMS is plain text. No buttons. No images. No formatting. And TRAI regulations require "STOP" and "HELP" keywords in every message.

### The Ground Truth

SMS is not a conversation channel. It is a notification and action channel. Use it for what it is good at: alerts, reminders, one-click actions. If you need a conversation, use chat or WhatsApp.`
  },
  {
    id: 'whatsapp-channel',
    title: 'WhatsApp: 500 Million Users. Highest Expectations.',
    summary: 'WhatsApp is the 800-pound gorilla of Indian customer communication. 500 million users. 98% open rates. Rich media. But it is also the most walled garden — Meta controls everything, and the 24-hour service window is a constant pressure.',
    readTime: '5 min',
    content: `WhatsApp is the channel everyone wants and most get wrong. Customers use WhatsApp to talk to their family and friends. When they message a business on WhatsApp, they expect the same speed, personality, and convenience. A slow, robotic, form-filling bot on WhatsApp feels like a betrayal of the platform.

### The Walled Garden

WhatsApp Business API has three constraints that most teams discover too late:

**1. Template approval takes 2-7 days.** Every message you send proactively must use a pre-approved template. Meta reviews every single one. Rejection is common.

**2. The 24-hour window.** After a customer messages you, you have 24 hours to respond with free-form messages. After that, you can only send templates. Long-running conversations get cut off.

**3. Opt-in proof is required.** Meta audits require proof that every customer opted in. Without a CRM to store this, your business account can get suspended.

### The Ops-Product-Tech Gap in WhatsApp

**Ops** wants to send proactive messages to drive engagement and revenue.

**Product** wants rich, interactive experiences with buttons, lists, and media.

**Tech** knows that every proactive message needs an approved template, every customer needs opt-in proof, and the 24-hour window is a hard deadline.

### The Ground Truth

WhatsApp has the highest expectations. Customers use it to talk to their mothers. If your bot feels like a form, they will block you. Short messages. Buttons not typing. Personality not corporate-speak. Get that right, and WhatsApp will be your highest-CSAT channel.`
  },
  {
    id: 'l1-framework',
    title: 'The L1 Framework: 15 Phases to a Bot That Actually Works',
    summary: 'After four failed deployments and Rs 18L in lessons, this is the field manual I wish someone had handed me before the first one. Fifteen phases. Five channels. Zero fluff.',
    readTime: '8 min',
    content: `I have built bots that failed spectacularly. One cost Rs 18L and six months — and it answered exactly 23 queries correctly before we pulled the plug. Another hit 92% resolution rate in testing and 34% in production because we tested on scripted queries, not real ones.

This framework is what I learned the hard way.

### The 15 Phases

**Phase 0: Don't Build Yet.** Three questions you must answer before spending a single rupee. Do you have six months of query data? Is your manual process documented? Do you have a human who will own the bot post-launch?

**Phase 1: Define the Bot.** The Bot Identity Card — name, personality, scope, channels, languages, hours, escalation target, KB minimum, max turns. Fill this out before writing code.

**Phase 2: Build the KB.** Fifty articles minimum before soft launch. Each tested against 50 real queries. No exceptions.

**Phase 3: Data Architecture.** What data you need, the database schema, the Monday Morning Ritual — 30 minutes every week to review escalations and fix gaps.

**Phase 4: Pricing and ROI.** The real cost of building a bot (Rs 23-39L in-house, Rs 8-18L vendor) and how to calculate ROI honestly.

**Phase 5: Capability Ceiling.** What a basic L1 bot can and cannot do. Spoiler: it cannot handle angry customers, process refunds, or remember context from previous chats.

**Phase 6: Interruption and Latency.** The 2-second rule, the typing indicator trap, and how to handle customers who interrupt mid-response.

**Phase 7: Bot SOPs.** Every flow documented. Every escalation trigger defined. Every failure reason logged.

**Phase 8: Why Bots Fail.** The top 10 reasons, the Day 1 reality (60% correct, 25% escalate, 10% wrong, 5% break), and the 3-month degradation curve.

**Phases 9-15:** Outbound and Renewal Engine, Lead Generation, CRM Integration, Telephony, In-House vs Vendor, Marketing Cloud, and Success Metrics.

### The Full Document

The complete 8,600-word field manual is available for download. It covers all five channels — voice, chat, email, SMS, and WhatsApp — with setup requirements, CRM needs, reporting dashboards, and the real reasons bots fail.

[Download the full framework]

This is not theory. This is ground truth from someone who has been in the trenches of Indian call centers — where agents quit without notice, power cuts happen at 3 PM, customers yell in Hinglish, and the CRM goes down every other Tuesday.`
  }
]

export function AlignmentTab() {
  const [selected, setSelected] = useState<string | null>(null)
  const [publishedIndex, setPublishedIndex] = useState(7)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/v1/alignment/status')
      .then(r => r.json())
      .then(d => {
        setPublishedIndex(d.current_index)
        setLoading(false)
      })
      .catch(() => {
        setPublishedIndex(7)
        setLoading(false)
      })
  }, [])

  const visibleArticles = ARTICLES.slice(0, publishedIndex)
  const article = selected ? ARTICLES.find(a => a.id === selected) : null

  if (article) {
    return (
      <div style={{ padding: '40px 48px', maxWidth: 800 }}>
        <button onClick={() => setSelected(null)}
          style={{ background: 'transparent', border: '1px solid oklch(34% 0.005 240)', color: 'oklch(72% 0.005 240)', fontSize: 12, padding: '6px 12px', cursor: 'pointer', fontFamily: 'inherit', marginBottom: 24 }}>
          &larr; Back to all articles
        </button>
        <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(72% 0.18 215)', marginBottom: 8 }}>The Alignment Gap &mdash; {article.readTime} read</div>
        <div style={{ fontSize: 28, lineHeight: '36px', fontWeight: 600, letterSpacing: '-0.01em', marginBottom: 16 }}>{article.title}</div>
        <div style={{ fontSize: 14, lineHeight: '22px', color: 'oklch(72% 0.005 240)', marginBottom: 24, whiteSpace: 'pre-wrap' }}>{article.content}</div>
        <div style={{ borderTop: '1px solid oklch(26% 0.005 240)', paddingTop: 16, marginTop: 16 }}>
          <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(55% 0.005 240)' }}>Kailas Swami &mdash; Digital Revenue Lead at Quick Heal</div>
          <div style={{ fontSize: 12, color: 'oklch(55% 0.005 240)', marginTop: 4 }}>Service + AI, run as an operating system.</div>
        </div>
      </div>
    )
  }

  return (
    <div style={{ padding: '40px 48px', maxWidth: 1000 }}>
      <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(72% 0.18 215)', marginBottom: 8 }}>The Alignment Gap</div>
      <div style={{ fontSize: 32, lineHeight: '40px', fontWeight: 600, letterSpacing: '-0.01em', maxWidth: 600 }}>Why service bots fail isn't a technology problem.</div>
      <div style={{ fontSize: 14, lineHeight: '22px', color: 'oklch(72% 0.005 240)', marginTop: 12, maxWidth: 560 }}>
        Every bot I have seen fail &mdash; and I have seen enough &mdash; failed because Operations, Product, and Technology teams built three different bots. This series explores the gap between them and how to bridge it.
      </div>
      {loading ? (
        <div style={{ marginTop: 32, fontFamily: '"Geist Mono", monospace', fontSize: 12, color: 'oklch(55% 0.005 240)' }}>Loading...</div>
      ) : (
        <>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 32 }}>
            {visibleArticles.map((a, i) => (
              <div key={a.id} onClick={() => setSelected(a.id)}
                style={{ border: '1px solid oklch(26% 0.005 240)', padding: 20, cursor: 'pointer', background: 'oklch(14% 0.005 240)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
                  <span style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, color: 'oklch(55% 0.005 240)' }}>0{i + 1}</span>
                  <span style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, color: 'oklch(72% 0.18 215)' }}>{a.readTime} read</span>
                </div>
                <div style={{ fontSize: 18, fontWeight: 500, lineHeight: '26px' }}>{a.title}</div>
                <div style={{ fontSize: 13, lineHeight: '20px', color: 'oklch(72% 0.005 240)', marginTop: 6 }}>{a.summary}</div>
              </div>
            ))}
          </div>
          {publishedIndex < 7 && (
            <div style={{ marginTop: 16, fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(55% 0.005 240)' }}>
              Next article publishes tomorrow at 10 AM IST. {7 - publishedIndex} articles remaining.
            </div>
          )}
          <div style={{ marginTop: 32, border: '1px solid oklch(26% 0.005 240)', padding: 20, background: 'oklch(14% 0.005 240)' }}>
            <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(55% 0.005 240)', marginBottom: 8 }}>Download the full field manual</div>
            <div style={{ fontSize: 14, lineHeight: '22px', color: 'oklch(72% 0.005 240)' }}>
              The complete 8,600-word L1 Automation Field Manual covers all five channels with setup requirements, CRM needs, reporting dashboards, and the real reasons bots fail.
            </div>
            <a href="/docs/L1-Query-Automation-Framework.md" target="_blank"
              style={{ display: 'inline-block', marginTop: 12, background: 'oklch(72% 0.18 215)', color: 'oklch(8% 0 0)', fontWeight: 500, fontSize: 13, padding: '10px 16px', textDecoration: 'none', fontFamily: 'inherit' }}>
              Download the field manual &rarr;
            </a>
          </div>
        </>
      )}
    </div>
  )
}
