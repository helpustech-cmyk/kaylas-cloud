import { knowledgeBase, fallbackAnswer } from '../data/knowledge'

// Simple keyword-overlap retrieval. Swappable later for a real vector DB
// (Pinecone/ChromaDB + embeddings) behind the same answer(query) signature.
export function answer(query: string): string {
  const q = query.toLowerCase()
  let best = { score: 0, answer: fallbackAnswer }

  for (const entry of knowledgeBase) {
    const score = entry.keywords.reduce(
      (acc, kw) => (q.includes(kw) ? acc + kw.length : acc),
      0,
    )
    if (score > best.score) {
      best = { score, answer: entry.answer }
    }
  }

  return best.answer
}
