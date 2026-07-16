// Static content for the About / News / Research / Repos / Training / Social
// tabs. Sourced from the site's design brief (Docs/design export, 2026-07-09)
// and cross-checked against BLUEPRINT.md phase plan — items not yet real
// (e.g. auto-published news, repos, training videos) are labelled as such
// rather than presented as live data.

export interface NewsItem {
  rank: number
  title: string
  summary: string
  meta: string
}

// Sample only — becomes a real hourly n8n pull once Phase 3 (automation) ships.
export const aiNews: NewsItem[] = [
  {
    rank: 1,
    title: 'DeepSeek-V4 tops open-weights leaderboard on 1/10th the training compute',
    summary:
      'Mixture-of-experts routing breakthrough halves inference cost — infra teams everywhere re-run their GPU math.',
    meta: 'sample data',
  },
  {
    rank: 2,
    title: 'NVIDIA opens NVLink to custom silicon — hyperscalers respond in hours',
    summary: 'The interconnect moat cracks; analysts call it the biggest AI-infra shift of the year.',
    meta: 'sample data',
  },
  {
    rank: 3,
    title: 'Multi-agent teams beat single large models on long-horizon tasks',
    summary:
      'Cheap small models orchestrated as agent teams outperform one large model — big implications for CX automation.',
    meta: 'sample data',
  },
  {
    rank: 4,
    title: 'Regulators require customer-facing bots to disclose AI identity',
    summary: 'Every service org running voice or chat AI now needs a disclosure layer.',
    meta: 'sample data',
  },
  {
    rank: 5,
    title: 'Quantum error correction milestone: logical qubit runs 24h stable',
    summary: 'Still years from breaking real workloads — but quantum-AI hybrid scheduling is now a research field.',
    meta: 'sample data',
  },
]

export interface ResearchTopic {
  tag: string
  title: string
}

export const researchTopics: ResearchTopic[] = [
  { tag: 'agentic ai', title: 'Agent teams replacing manual workflows' },
  { tag: 'quantum ai', title: 'Quantum-AI hybrids, explained simply' },
  { tag: 'ai infra', title: 'The GPU economy and who profits' },
  { tag: 'service + ai', title: 'Frontline teams in the AI era' },
  { tag: 'cx psychology', title: 'Customer psychology meets ML' },
  { tag: 'future jobs', title: 'Where AI jobs land in the next decade' },
]

export interface RepoItem {
  name: string
  description: string
  visibility: 'public' | 'private' | 'planned'
}

export const repos: RepoItem[] = [
  { name: 'kaylas-cloud', description: 'This website — React + Vite, auto-deployed to Vercel on push', visibility: 'public' },
  { name: 'kaylas-twin-brain', description: 'RAG API for the AI twin: knowledge base + retrieval, planned upgrade to a real vector DB', visibility: 'planned' },
  { name: 'kaylas-automations', description: 'n8n workflows: AI-news pull, social publisher, weekly report', visibility: 'planned' },
  { name: 'kaylas-infra', description: 'VPS provisioning — docker-compose, reverse proxy, backups', visibility: 'planned' },
]

export interface TrainingItem {
  title: string
  meta: string
}

export const trainings: TrainingItem[] = [
  { title: 'From service cost center to revenue engine', meta: 'framework — coming soon' },
  { title: 'NPS and CSAT: metrics that change behavior', meta: 'video series — coming soon' },
  { title: 'Upskilling frontline staff for the AI era', meta: 'playbook — coming soon' },
]

export interface SocialChannel {
  channel: string
  note: string
  status: string
}

export const socialChannels: SocialChannel[] = [
  { channel: 'LinkedIn', note: 'Career posts and CX + AI commentary.', status: 'connect in a later automation phase' },
  { channel: 'X / Twitter', note: 'Short takes on AI infra news.', status: 'connect in a later automation phase' },
  { channel: 'Telegram', note: 'Broadcast channel for new research posts.', status: 'connect in a later automation phase' },
]

export const heroQuickLinks = [
  { tabId: 'news' as const, label: 'Latest AI news' },
  { tabId: 'research' as const, label: 'Research lab' },
  { tabId: 'resume' as const, label: 'Resume' },
]
