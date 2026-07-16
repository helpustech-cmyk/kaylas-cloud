import { stats, summary } from '../../data/resume'
import { aiNews } from '../../data/content'
import { TwinAvatar } from '../TwinAvatar'
import type { TabId } from '../../lib/navigation'

interface AboutTabProps {
  onNavigate: (tabId: TabId) => void
  talking?: boolean
  listening?: boolean
}

export function AboutTab({ onNavigate, talking = false, listening = false }: AboutTabProps) {
  return (
    <div style={{ flex: 1, position: 'relative', overflow: 'hidden', background: 'oklch(10% 0.005 240)' }}>
      <div style={{ position: 'relative', display: 'flex', alignItems: 'center', gap: 24, padding: 48 }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(72% 0.18 215)', marginBottom: 16 }}>Digital revenue leader - AI infrastructure - Quick Heal</div>
          <div style={{ fontSize: 44, lineHeight: '52px', fontWeight: 600, letterSpacing: '-0.01em' }}>Kailas Swami.<br />Service + AI, run as<br />an operating system.</div>
          <div style={{ fontSize: 14, lineHeight: '22px', color: 'oklch(72% 0.005 240)', marginTop: 16, maxWidth: 460 }}>{summary}</div>
          <div style={{ display: 'flex', gap: 24, marginTop: 24, fontFamily: '"Geist Mono", monospace', fontSize: 12, color: 'oklch(72% 0.005 240)' }}>
            {stats.map(s => (<span key={s.label}><span style={{ color: 'oklch(96% 0.005 240)', fontSize: 18 }}>{s.value}</span> {s.label}</span>))}
          </div>
        </div>
        <div style={{ width: 340, flex: 'none', position: 'relative' }}>
          <TwinAvatar talking={talking} listening={listening} />
        </div>
      </div>
      <div style={{ position: 'relative', display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8, padding: '0 48px 40px' }}>
        <div onClick={() => onNavigate('news')} style={{ border: '1px solid oklch(26% 0.005 240)', background: 'oklch(14% 0.005 240)', padding: 16, cursor: 'pointer' }}>
          <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(55% 0.005 240)' }}>Latest AI news</div>
          <div style={{ fontSize: 13, lineHeight: '20px', marginTop: 8 }}>{aiNews[0]?.title || 'Loading...'}</div>
          <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(72% 0.18 215)', marginTop: 8 }}>open ai-news -&gt;</div>
        </div>
        <div onClick={() => onNavigate('research')} style={{ border: '1px solid oklch(26% 0.005 240)', background: 'oklch(14% 0.005 240)', padding: 16, cursor: 'pointer' }}>
          <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(55% 0.005 240)' }}>Research lab</div>
          <div style={{ fontSize: 13, lineHeight: '20px', marginTop: 8 }}>Agentic AI - Quantum AI - where AI jobs land next decade</div>
          <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(72% 0.18 215)', marginTop: 8 }}>open research -&gt;</div>
        </div>
        <div onClick={() => onNavigate('resume')} style={{ border: '1px solid oklch(26% 0.005 240)', background: 'oklch(14% 0.005 240)', padding: 16, cursor: 'pointer' }}>
          <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(55% 0.005 240)' }}>Resume</div>
          <div style={{ fontSize: 13, lineHeight: '20px', marginTop: 8 }}>8 roles - MBA - PMP training - Six Sigma (pursuing)</div>
          <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(72% 0.18 215)', marginTop: 8 }}>open resume -&gt;</div>
        </div>
      </div>
    </div>
  )
}
