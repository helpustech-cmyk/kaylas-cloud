import { aiNews } from '../../data/content'

export function NewsTab() {
  return (
    <div style={{ padding: '40px 48px', maxWidth: 900 }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 12 }}>
        <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(72% 0.18 215)' }}>03 - AI news - top 5 viral</div>
        <span style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, color: 'oklch(55% 0.005 240)' }}>sample data - auto-pulled hourly once n8n phase 3 is live</span>
      </div>
      <div style={{ fontSize: 32, lineHeight: '40px', fontWeight: 600, letterSpacing: '-0.01em', marginTop: 8 }}>AI infra and research, ranked by the robots</div>
      <div style={{ marginTop: 24, display: 'flex', flexDirection: 'column', gap: 8 }}>
        {aiNews.map(n => (
          <div key={n.rank} style={{ border: '1px solid oklch(26% 0.005 240)', padding: 16, display: 'flex', gap: 16 }}>
            <span style={{ fontFamily: '"Geist Mono", monospace', fontSize: 20, color: 'oklch(72% 0.18 215)', flex: 'none', width: 28 }}>{n.rank}</span>
            <div style={{ minWidth: 0 }}>
              <div style={{ fontSize: 14, fontWeight: 500, lineHeight: '22px' }}>{n.title}</div>
              <div style={{ fontSize: 13, lineHeight: '20px', color: 'oklch(72% 0.005 240)', marginTop: 4 }}>{n.summary}</div>
              <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(55% 0.005 240)', marginTop: 8 }}>{n.meta}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
