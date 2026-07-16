interface GlyphFaceProps {
  talking?: boolean
  cell?: number
  style?: React.CSSProperties
}

export function GlyphFace({ talking = false, style }: GlyphFaceProps) {
  const cols = 16
  const rows = Math.ceil(380 / (320 / cols))
  const cellSize = 320 / cols
  const glyphs = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'

  function getGlyph(r: number, c: number) {
    const cx = c - cols / 2
    const cy = r - rows / 2
    const dist = Math.sqrt(cx * cx + cy * cy)
    const faceRx = cols * 0.38
    const faceRy = rows * 0.45
    const inFace = (cx * cx) / (faceRx * faceRx) + (cy * cy) / (faceRy * faceRy) <= 1
    if (!inFace) return { char: '', opacity: 0 }
    const eyeY = -rows * 0.12
    const eyeX = cols * 0.2
    if (Math.abs(cy - eyeY) < 2 && (Math.abs(cx + eyeX) < 2.5 || Math.abs(cx - eyeX) < 2.5)) {
      return { char: '◉', opacity: 0.9 }
    }
    const mouthY = rows * 0.2
    const mouthOpen = talking ? 3 : 1.5
    if (Math.abs(cy - mouthY) < mouthOpen && Math.abs(cx) < cols * 0.2) {
      return { char: talking ? '◊' : '─', opacity: 0.8 }
    }
    const idx = Math.floor(Math.random() * glyphs.length)
    const bright = 0.3 + 0.7 * (1 - dist / Math.max(cols, rows))
    return { char: glyphs[idx], opacity: Math.max(0.15, bright) }
  }

  return (
    <div style={{ width: 320, height: 380, position: 'relative', ...style }}>
      <svg viewBox={'0 0 ' + (cols * cellSize) + ' ' + (rows * cellSize)} width={320} height={380}>
        {Array.from({ length: rows }, (_, r) =>
          Array.from({ length: cols }, (_, c) => {
            const { char, opacity } = getGlyph(r, c)
            if (!char) return null
            return (
              <text
                key={r + '-' + c}
                x={c * cellSize + cellSize / 2}
                y={r * cellSize + cellSize * 0.7}
                textAnchor="middle"
                fontFamily="'Geist Mono', monospace"
                fontSize={cellSize * 0.8}
                fill={'oklch(72% 0.18 215 / ' + opacity + ')'}
              >
                {char}
              </text>
            )
          })
        )}
      </svg>
    </div>
  )
}
