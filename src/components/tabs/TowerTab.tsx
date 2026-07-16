import { useState } from 'react'

export function TowerTab() {
  const [unlocked, setUnlocked] = useState(false)
  if (!unlocked) {
    return (
      <div style={{ padding: '40px 48px', maxWidth: 420 }}>
        <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(72% 0.18 215)' }}>08 - Admin control tower</div>
        <div style={{ marginTop: 24, border: '1px solid oklch(26% 0.005 240)', padding: 32 }}>
          <div style={{ fontSize: 16, fontWeight: 600 }}>Owner only</div>
          <div style={{ fontSize: 13, lineHeight: '20px', color: 'oklch(72% 0.005 240)', marginTop: 8 }}>This tab shows live container health, automation runs, leads, and affiliate clicks from status.json.</div>
          <button onClick={() => setUnlocked(true)} style={{ marginTop: 16, background: 'oklch(72% 0.18 215)', color: 'oklch(8% 0 0)', fontWeight: 500, fontSize: 13, padding: '10px 16px', border: 0, cursor: 'pointer', fontFamily: 'inherit' }}>Enter as owner (demo)</button>
        </div>
      </div>
    )
  }
  const towerStats = [
    { label: 'Uptime 30d', value: '99.98%', sub: 'all monitors green' },
    { label: 'Chats today', value: '23', sub: '4 leads captured' },
    { label: 'News runs', value: '24/24', sub: 'last 12m ago' },
    { label: 'Affiliate clicks', value: '31', sub: 'this week' },
  ]
  const containers = [
    { name: 'caddy', state: 'running', res: '0.1% cpu - 24MB' },
    { name: 'n8n', state: 'running', res: '1.2% cpu - 210MB' },
    { name: 'twin-brain', state: 'running', res: '0.8% cpu - 145MB' },
    { name: 'chromadb', state: 'running', res: '0.4% cpu - 320MB' },
    { name: 'ollama', state: 'running', res: 'idle - 2.1GB' },
  ]
  return (
    <div style={{ padding: '40px 48px', maxWidth: 1000 }}>
      <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(72% 0.18 215)' }}>08 - Admin control tower</div>
      <div style={{ fontSize: 32, lineHeight: '40px', fontWeight: 600, letterSpacing: '-0.01em', marginTop: 8 }}>Everything running, one glance</div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8, marginTop: 24 }}>
        {towerStats.map(ts => (
          <div key={ts.label} style={{ border: '1px solid oklch(26% 0.005 240)', padding: 16 }}>
            <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(55% 0.005 240)' }}>{ts.label}</div>
            <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 22, marginTop: 8, color: 'oklch(96% 0.005 240)' }}>{ts.value}</div>
            <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(60% 0.14 160)', marginTop: 4 }}>{ts.sub}</div>
          </div>
        ))}
      </div>
      <div style={{ marginTop: 16, border: '1px solid oklch(26% 0.005 240)' }}>
        <div style={{ padding: '10px 16px', borderBottom: '1px solid oklch(26% 0.005 240)', fontFamily: '"Geist Mono", monospace', fontSize: 10, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(55% 0.005 240)' }}>Containers</div>
        {containers.map(c => (
          <div key={c.name} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '10px 16px', borderBottom: '1px solid oklch(26% 0.005 240)', fontFamily: '"Geist Mono", monospace', fontSize: 12 }}>
            <span style={{ display: 'inline-block', width: 7, height: 7, borderRadius: 9999, background: 'oklch(60% 0.14 160)' }}></span>
            <span style={{ width: 160 }}>{c.name}</span>
            <span style={{ color: 'oklch(72% 0.005 240)' }}>{c.state}</span>
            <span style={{ marginLeft: 'auto', color: 'oklch(55% 0.005 240)' }}>{c.res}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
