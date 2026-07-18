export type TabId = 'about' | 'resume' | 'news' | 'research' | 'repos' | 'training' | 'social' | 'tower' | 'alignment'

const NAV_INTENTS: { tab: TabId; keywords: string[] }[] = [
  { tab: 'resume', keywords: ['resume', 'cv'] },
  { tab: 'news', keywords: ['ai news', 'news'] },
  { tab: 'research', keywords: ['research', 'blog', 'knowledge lab'] },
  { tab: 'repos', keywords: ['repo', 'github', 'automation project'] },
  { tab: 'training', keywords: ['training'] },
  { tab: 'social', keywords: ['social', 'linkedin', 'twitter'] },
  { tab: 'tower', keywords: ['tower', 'admin', 'control'] },
  { tab: 'about', keywords: ['about', 'home', 'overview'] },
  { tab: 'alignment', keywords: ['alignment', 'gap', 'playbook', 'field manual', 'bot failure'] },
]

export function resolveNavIntent(query: string): TabId | null {
  const q = query.toLowerCase()
  if (!/\b(open|show|go to|take me|navigate)\b/.test(q)) return null
  for (const intent of NAV_INTENTS) {
    if (intent.keywords.some((kw) => q.includes(kw))) return intent.tab
  }
  return null
}
