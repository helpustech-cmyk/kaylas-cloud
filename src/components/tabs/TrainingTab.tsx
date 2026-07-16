import { trainings } from '../../data/content'

export function TrainingTab() {
  return (
    <div style={{ padding: '40px 48px', maxWidth: 1000 }}>
      <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(72% 0.18 215)' }}>06 - Service leaders training</div>
      <div style={{ fontSize: 32, lineHeight: '40px', fontWeight: 600, letterSpacing: '-0.01em', marginTop: 8 }}>Upskilling frontline leaders for the AI era</div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8, marginTop: 24 }}>
        {trainings.map(tr => (
          <div key={tr.title} style={{ border: '1px solid oklch(26% 0.005 240)' }}>
            <div style={{ aspectRatio: '16/9', background: 'oklch(10% 0.005 240)', display: 'grid', placeItems: 'center', fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(55% 0.005 240)' }}>video placeholder</div>
            <div style={{ padding: '12px 16px' }}>
              <div style={{ fontSize: 13, fontWeight: 500, lineHeight: '20px' }}>{tr.title}</div>
              <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(55% 0.005 240)', marginTop: 4 }}>{tr.meta}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
