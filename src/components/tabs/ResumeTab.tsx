import { useState } from 'react'
import { achievements, education, jobs } from '../../data/resume'

export function ResumeTab() {
  const [openJob, setOpenJob] = useState<string | null>(jobs[0]?.company || null)
  return (
    <div style={{ padding: '40px 48px', maxWidth: 900 }}>
      <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(72% 0.18 215)' }}>02 - Resume</div>
      <div style={{ fontSize: 32, lineHeight: '40px', fontWeight: 600, letterSpacing: '-0.01em', marginTop: 8 }}>14 years, 6 months in service - now Service + AI</div>
      <div style={{ marginTop: 24, borderTop: '1px solid oklch(26% 0.005 240)' }}>
        {jobs.map(job => {
          const isOpen = openJob === job.company
          return (
            <details key={job.company} className="om-role" open={isOpen} style={{ borderBottom: '1px solid oklch(26% 0.005 240)' }}>
              <summary onClick={() => setOpenJob(isOpen ? null : job.company)}
                style={{ display: 'flex', alignItems: 'baseline', gap: 12, padding: '14px 8px', cursor: 'pointer', listStyle: 'none' }}>
                <span style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(55% 0.005 240)', width: 110, flex: 'none' }}>{job.dates}</span>
                <span style={{ fontWeight: 500, fontSize: 14 }}>{job.company}</span>
                <span style={{ color: 'oklch(72% 0.005 240)', fontSize: 13 }}>{job.title}</span>
                <span style={{ marginLeft: 'auto', fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(55% 0.005 240)' }}>{isOpen ? String.fromCharCode(0x25B2) : String.fromCharCode(0x25BC)}</span>
              </summary>
              <div style={{ padding: '0 8px 16px 130px', fontSize: 13, lineHeight: '20px', color: 'oklch(72% 0.005 240)' }}>
                {job.bullets.map((b, i) => <div key={i}>{b}</div>)}
              </div>
            </details>
          )
        })}
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginTop: 24 }}>
        <div style={{ border: '1px solid oklch(26% 0.005 240)', padding: 16 }}>
          <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(55% 0.005 240)', marginBottom: 8 }}>Education</div>
          <div style={{ fontSize: 13, lineHeight: '22px', color: 'oklch(72% 0.005 240)' }}>{education.map((e, i) => <div key={i}>{e}</div>)}</div>
        </div>
        <div style={{ border: '1px solid oklch(26% 0.005 240)', padding: 16 }}>
          <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(55% 0.005 240)', marginBottom: 8 }}>Key wins</div>
          <div style={{ fontSize: 13, lineHeight: '22px', color: 'oklch(72% 0.005 240)' }}>{achievements.map((a, i) => <div key={i}>{a}</div>)}</div>
        </div>
      </div>
    </div>
  )
}
