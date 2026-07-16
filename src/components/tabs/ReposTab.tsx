import { repos } from '../../data/content'

export function ReposTab() {
  return (
    <div style={{ padding: '40px 48px', maxWidth: 900 }}>
      <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(72% 0.18 215)' }}>05 - Automation repos</div>
      <div style={{ fontSize: 32, lineHeight: '40px', fontWeight: 600, letterSpacing: '-0.01em', marginTop: 8 }}>The work is the portfolio</div>
      <div style={{ marginTop: 24, borderTop: '1px solid oklch(26% 0.005 240)' }}>
        {repos.map(rp => (
          <div key={rp.name} style={{ display: 'flex', alignItems: 'baseline', gap: 12, padding: '14px 8px', borderBottom: '1px solid oklch(26% 0.005 240)' }}>
            <span style={{ fontFamily: '"Geist Mono", monospace', fontSize: 12, color: 'oklch(72% 0.18 215)', width: 200, flex: 'none' }}>{rp.name}</span>
            <span style={{ fontSize: 13, color: 'oklch(72% 0.005 240)' }}>{rp.description}</span>
            <span style={{ marginLeft: 'auto', fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(55% 0.005 240)' }}>{rp.visibility}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
