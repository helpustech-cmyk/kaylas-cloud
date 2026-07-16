import { useEffect, useState } from 'react'

interface BootSeqProps {
  lines: string
  speed?: number
  style?: React.CSSProperties
}

export function BootSeq({ lines, speed = 14, style }: BootSeqProps) {
  const [visible, setVisible] = useState(0)
  const parts = lines.split('|')

  useEffect(() => {
    if (visible >= parts.length) return
    const t = setTimeout(() => setVisible((v) => v + 1), speed * 100 + Math.random() * 200)
    return () => clearTimeout(t)
  }, [visible, parts.length, speed])

  return (
    <div style={{ fontFamily: "'Geist Mono', monospace", fontSize: 14, lineHeight: '24px', color: 'oklch(60% 0.14 160)', ...style }}>
      {parts.slice(0, visible).map((line, i) => (
        <div key={i}>{line}</div>
      ))}
      {visible < parts.length && (
        <span style={{ animation: 'om-blink 1s step-end infinite' }}>|</span>
      )}
    </div>
  )
}
