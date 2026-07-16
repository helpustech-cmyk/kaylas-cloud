import { researchTopics } from '../../data/content'

export function ResearchTab() {
  return (
    <div style={{ padding: '40px 48px', maxWidth: 1000 }}>
      <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(72% 0.18 215)' }}>04 - Research lab and knowledge hub</div>
      <div style={{ fontSize: 32, lineHeight: '40px', fontWeight: 600, letterSpacing: '-0.01em', marginTop: 8 }}>Where AI jobs land in the next decade</div>
      <div style={{ fontSize: 13, lineHeight: '20px', color: 'oklch(72% 0.005 240)', marginTop: 8, maxWidth: 560 }}>Papers and blogs publish here automatically after passing the comprehension test in the tower.</div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8, marginTop: 24 }}>
        {researchTopics.map(rt => (
          <div key={rt.tag} style={{ border: '1px solid oklch(26% 0.005 240)', padding: 16, minHeight: 140, display: 'flex', flexDirection: 'column' }}>
            <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(55% 0.005 240)' }}>{rt.tag}</div>
            <div style={{ fontSize: 15, fontWeight: 500, lineHeight: '22px', marginTop: 8 }}>{rt.title}</div>
            <div style={{ marginTop: 'auto', fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(55% 0.005 240)' }}>0 posts - awaiting first draft</div>
          </div>
        ))}
      </div>
    </div>
  )
}
