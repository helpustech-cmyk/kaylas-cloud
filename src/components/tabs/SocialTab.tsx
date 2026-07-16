import { socialChannels } from '../../data/content'

export function SocialTab() {
  return (
    <div style={{ padding: '40px 48px', maxWidth: 1000 }}>
      <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(72% 0.18 215)' }}>07 - Social wall</div>
      <div style={{ fontSize: 32, lineHeight: '40px', fontWeight: 600, letterSpacing: '-0.01em', marginTop: 8 }}>One grid, every channel</div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8, marginTop: 24 }}>
        {socialChannels.map(s => (
          <div key={s.channel} style={{ border: '1px solid oklch(26% 0.005 240)', padding: 16, minHeight: 120, display: 'flex', flexDirection: 'column' }}>
            <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(72% 0.18 215)' }}>{s.channel}</div>
            <div style={{ fontSize: 13, lineHeight: '20px', color: 'oklch(72% 0.005 240)', marginTop: 8 }}>{s.note}</div>
            <div style={{ marginTop: 'auto', fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(55% 0.005 240)' }}>{s.status}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
