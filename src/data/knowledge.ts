export interface KnowledgeEntry {
  id: string
  keywords: string[]
  answer: string
}

// Sourced from the user's CV (see docs/CV_SOURCE.md) layered with the
// current role from BLUEPRINT.md. Swappable for a vector DB later — the
// retrieval layer only depends on the answer(query) signature in
// src/lib/retrieval.ts, not on how entries are stored.
export const knowledgeBase: KnowledgeEntry[] = [
  {
    id: 'role',
    keywords: ['role', 'job', 'current', 'work', 'quick heal', 'title', 'position', 'doing now'],
    answer:
      "I'm the Digital Revenue Lead at Quick Heal, a role I've held since September 2025. I own the customer lifecycle end to end — service, retention, cross-sell and up-sell.",
  },
  {
    id: 'summary',
    keywords: ['summary', 'about you', 'background', 'introduce', 'who are you', 'experience'],
    answer:
      "I have an MBA and 14+ years in the service industry. I've led call center teams of 130-165+ service experts plus 8+ vendors, working across IVR, email bots, speech analytics, and CRM development to turn service centers into profitable, compliant, customer-first operations.",
  },
  {
    id: 'ai-expertise',
    keywords: ['ai', 'artificial intelligence', 'machine learning', 'expertise', 'skills', 'digital transformation'],
    answer:
      'My core expertise spans marketing cloud and service tools, telephony systems, lead generation, and customer communication — and increasingly, applying AI and machine learning to CX: IVR revamps, chat bots, and speech analytics.',
  },
  {
    id: 'metrics',
    keywords: ['nps', 'csat', 'metrics', 'retention', 'revenue', 'personalization', 'kpi', 'achievement', 'results'],
    answer:
      'Some results I\'m proud of: raised service levels by 21% to hit 96%, cut repeat calls from 33% to 17%, reduced resolution time by 26% across 38 workflow fixes, and lifted home loan retention from 49% to 76%.',
  },
  {
    id: 'leadership',
    keywords: ['vendor', 'management', 'hiring', 'process', 'crm', 'operations', 'team'],
    answer:
      "On the operations side I run vendor management and hiring, process optimization, and CRM implementation — I've managed billing and service for 8+ vendors with zero audit discrepancies.",
  },
  {
    id: 'history-recent',
    keywords: ['parag milk', 'l&t', 'l and t finance', 'idfc', 'previous role', 'past job', 'career history'],
    answer:
      "Before Quick Heal, I was Head Customer Service at Parag Milk Foods Limited (Dec 2024 - Sept 2025), Manager Customer Service at L&T Finance leading 130+ agents across 11 lines of business, and a Team Leader at IDFC FIRST Bank running personalized video banking service for HNI clients.",
  },
  {
    id: 'education',
    keywords: ['education', 'mba', 'degree', 'college', 'university', 'study'],
    answer:
      "I hold an MBA from Suresh Gyan Vihar University (2021-23, CGPA 7.8), and a B.Com from K.G. Joshi & N.G. Bedekar College of Commerce, Thane.",
  },
  {
    id: 'certifications',
    keywords: ['certification', 'certificate', 'pmp', 'six sigma', 'lean'],
    answer:
      "I've completed certifications in Start-Up Management and Lean Management, and I'm currently pursuing PMP, Six Sigma Green Belt, and Data Science with Python.",
  },
  {
    id: 'hobbies',
    keywords: ['hobby', 'hobbies', 'trekking', 'personal', 'free time', 'outside work'],
    answer:
      "Outside work I'm a trek leader — I've volunteered with Ultimate Hikers since 2014. I also enjoy writing, yoga, teaching, travel, and meditation.",
  },
  {
    id: 'future',
    keywords: ['future', 'transformation', 'automation', 'new world', 'digital transformation 4'],
    answer:
      "I'm leading the shift from pure service to 'Service + AI' — using automation to generate revenue and upskilling frontline teams for the AI era.",
  },
  {
    id: 'contact',
    keywords: ['contact', 'reach', 'email', 'hire', 'connect', 'linkedin'],
    answer:
      "I'd love to connect — use the contact panel on the left to book time or send a message and I'll get back to you directly.",
  },
]

export const fallbackAnswer =
  "I don't have that in my knowledge base yet — try asking about my current role, career history, key achievements, education, or how to get in touch."
