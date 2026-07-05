export interface KnowledgeEntry {
  id: string
  keywords: string[]
  answer: string
}

// MVP knowledge base for the AI avatar. Replace/extend with the real CV content
// once the resume PDF is provided — the retrieval layer doesn't care where
// entries come from, so swapping this for a vector DB later is a drop-in change.
export const knowledgeBase: KnowledgeEntry[] = [
  {
    id: 'role',
    keywords: ['role', 'job', 'current', 'work', 'quack heal', 'title', 'position'],
    answer:
      "I'm the Digital Revenue Lead at Quack Heal, where I own the customer lifecycle end to end — service, retention, cross-sell and up-sell.",
  },
  {
    id: 'ai-expertise',
    keywords: ['ai', 'artificial intelligence', 'machine learning', 'expertise', 'skills'],
    answer:
      'My core expertise spans marketing cloud and service tools, telephony systems, lead generation, and customer communication — and increasingly, applying AI and machine learning to CX and process engineering.',
  },
  {
    id: 'metrics',
    keywords: ['nps', 'csat', 'metrics', 'retention', 'revenue', 'personalization'],
    answer:
      "I'm an NPS and CSAT specialist. I focus on customer personalization and turning retention into a revenue driver, not just a cost center.",
  },
  {
    id: 'leadership',
    keywords: ['vendor', 'management', 'hiring', 'process', 'crm', 'operations'],
    answer:
      'On the operations side I run vendor management and hiring, process optimization, and CRM implementation across the customer service stack.',
  },
  {
    id: 'future',
    keywords: ['future', 'transformation', 'automation', 'new world', 'digital transformation'],
    answer:
      "I'm leading the shift from pure service to 'Service + AI' — using automation to generate revenue and upskilling frontline teams for the AI era.",
  },
  {
    id: 'contact',
    keywords: ['contact', 'reach', 'email', 'hire', 'connect'],
    answer:
      "I'd love to connect — use the contact panel on the left to book time or send a message and I'll get back to you directly.",
  },
]

export const fallbackAnswer =
  "I don't have that in my knowledge base yet — try asking about my current role, AI expertise, retention metrics, or how to get in touch."
