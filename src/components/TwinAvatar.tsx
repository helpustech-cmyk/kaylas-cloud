import { useRef, useEffect, useState } from 'react'

interface TwinAvatarProps {
  talking?: boolean
  listening?: boolean
  style?: React.CSSProperties
}

export function TwinAvatar({ talking = false, listening = false, style }: TwinAvatarProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    let raf = 0
    let t = 0

    const resize = () => {
      const rect = canvas.getBoundingClientRect()
      const dpr = Math.min(window.devicePixelRatio || 1, 2)
      canvas.width = Math.floor(rect.width * dpr)
      canvas.height = Math.floor(rect.height * dpr)
    }
    resize()
    window.addEventListener('resize', resize)

    const particles: { x: number; y: number; vx: number; vy: number; r: number; alpha: number; speed: number }[] = []
    const pCount = 360
    for (let i = 0; i < pCount; i++) {
      particles.push({
        x: Math.random(),
        y: Math.random(),
        vx: (Math.random() - 0.5) * 0.0004,
        vy: (Math.random() - 0.5) * 0.0004,
        r: 0.5 + Math.random() * 1.5,
        alpha: 0.1 + Math.random() * 0.5,
        speed: 0.2 + Math.random() * 0.6,
      })
    }

    const draw = () => {
      const rect = canvas.getBoundingClientRect()
      const w = rect.width
      const h = rect.height
      ctx.setTransform(1, 0, 0, 1, 0, 0)
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      const dpr = Math.min(window.devicePixelRatio || 1, 2)
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
      t += 0.012
      const cx = w / 2
      const cy = h / 2 - 8
      const fw = w * 0.58
      const fh = h * 0.74

      // deep navy background fill
      ctx.fillStyle = '#050B16'
      ctx.fillRect(0, 0, w, h)

      // vertical digital rain streaks
      ctx.save()
      ctx.globalCompositeOperation = 'screen'
      ctx.strokeStyle = 'rgba(66, 165, 245, 0.08)'
      ctx.lineWidth = 1
      for (let i = 0; i < 22; i++) {
        const x = (i / 21) * w + Math.sin(t * 0.4 + i) * 4
        const yOff = (t * 40 * (0.5 + (i % 5) / 5)) % (h + 80) - 40
        ctx.beginPath()
        ctx.moveTo(x, yOff)
        ctx.lineTo(x, yOff + 40 + Math.random() * 30)
        ctx.stroke()
      }
      ctx.restore()

      // floating particles / hair field
      ctx.save()
      ctx.globalCompositeOperation = 'screen'
      const intensity = talking ? 1.6 : listening ? 1.25 : 1
      for (const p of particles) {
        p.x += p.vx * (talking ? 3 : 1)
        p.y += p.vy * (talking ? 3 : 1)
        if (p.x < 0 || p.x > 1) p.vx *= -1
        if (p.y < 0 || p.y > 1) p.vy *= -1
        const px = p.x * w
        const py = p.y * h
        const pulse = p.alpha * intensity + Math.sin(t * p.speed * 2 + p.x * 10) * 0.1
        ctx.fillStyle = `rgba(0, 229, 255, ${Math.max(0, pulse)})`
        ctx.beginPath()
        ctx.arc(px, py, p.r, 0, Math.PI * 2)
        ctx.fill()
      }
      // thin links
      ctx.strokeStyle = `rgba(66, 165, 245, ${0.06 * intensity})`
      ctx.lineWidth = 0.4
      ctx.beginPath()
      for (let i = 0; i < pCount; i += 3) {
        const a = particles[i]
        for (let j = i + 1; j < pCount; j += Math.floor(pCount / 12)) {
          const b = particles[j]
          const dx = a.x - b.x
          const dy = a.y - b.y
          if (dx * dx + dy * dy < 0.02) {
            ctx.moveTo(a.x * w, a.y * h)
            ctx.lineTo(b.x * w, b.y * h)
          }
        }
      }
      ctx.stroke()
      ctx.restore()

      // holographic projection rings at neck
      ctx.save()
      ctx.globalCompositeOperation = 'screen'
      const ringY = cy + fh * 0.58
      const rings = [
        { r: fw * 0.55, alpha: 0.22 },
        { r: fw * 0.72, alpha: 0.14 },
        { r: fw * 0.90, alpha: 0.08 },
      ]
      for (let i = 0; i < rings.length; i++) {
        const rg = rings[i]
        const rot = t * (0.5 + i * 0.2)
        ctx.strokeStyle = `rgba(0, 229, 255, ${rg.alpha * intensity})`
        ctx.lineWidth = 1.2 - i * 0.3
        ctx.beginPath()
        ctx.ellipse(cx, ringY + i * 8, rg.r, rg.r * 0.18, rot, 0, Math.PI * 2)
        ctx.stroke()
      }
      ctx.restore()

      // polygon mesh face
      ctx.save()
      ctx.globalCompositeOperation = 'screen'
      ctx.strokeStyle = `rgba(0, 229, 255, ${0.09 * intensity})`
      ctx.lineWidth = 0.5
      const cols = 24
      const rows = 30
      const pts: { x: number; y: number }[][] = []
      for (let r = 0; r <= rows; r++) {
        pts[r] = []
        for (let c = 0; c <= cols; c++) {
          const nx = c / cols - 0.5
          const ny = r / rows - 0.5
          const fx = cx + nx * fw * (1 - ny * ny * 0.35)
          const fy = cy + ny * fh
          const drift = Math.sin(t * 1.2 + r * 0.4 + c * 0.3) * 1.2
          pts[r][c] = { x: fx + drift, y: fy }
        }
      }
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const p1 = pts[r][c], p2 = pts[r][c + 1], p4 = pts[r + 1][c + 1]
          ctx.beginPath()
          ctx.moveTo(p1.x, p1.y)
          ctx.lineTo(p2.x, p2.y)
          ctx.lineTo(p4.x, p4.y)
          ctx.closePath()
          ctx.stroke()
        }
      }
      ctx.restore()

      // neural nodes
      ctx.save()
      ctx.globalCompositeOperation = 'screen'
      const nodes = [
        { x: cx, y: cy - fh * 0.32, r: 3.5 },
        { x: cx - fw * 0.18, y: cy - fh * 0.06, r: 2.6 },
        { x: cx + fw * 0.18, y: cy - fh * 0.06, r: 2.6 },
        { x: cx, y: cy + fh * 0.12, r: 2.8 },
        { x: cx - fw * 0.14, y: cy + fh * 0.22, r: 2.4 },
        { x: cx + fw * 0.14, y: cy + fh * 0.22, r: 2.4 },
        { x: cx, y: cy + fh * 0.40, r: 3.2 },
        { x: cx, y: cy + fh * 0.62, r: 4.0 },
      ]
      for (const n of nodes) {
        const pulse = 1 + Math.sin(t * 2 + n.x) * 0.25
        const alpha = talking ? 0.45 : listening ? 0.35 : 0.28
        const g = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r * 5 * pulse)
        g.addColorStop(0, `rgba(0, 229, 255, ${alpha})`)
        g.addColorStop(0.5, `rgba(66, 165, 245, ${alpha * 0.4})`)
        g.addColorStop(1, 'rgba(0, 229, 255, 0)')
        ctx.fillStyle = g
        ctx.beginPath()
        ctx.arc(n.x, n.y, n.r * 5 * pulse, 0, Math.PI * 2)
        ctx.fill()
      }
      ctx.restore()

      // neural energy lines
      ctx.save()
      ctx.globalCompositeOperation = 'screen'
      ctx.strokeStyle = talking ? 'rgba(0, 229, 255, 0.22)' : listening ? 'rgba(66, 165, 245, 0.18)' : 'rgba(0, 229, 255, 0.14)'
      ctx.lineWidth = 0.8
      for (let i = 0; i < 16; i++) {
        const sx = cx - fw * 0.25 + Math.sin(t * 0.4 + i) * fw * 0.15
        const sy = cy - fh * 0.25 + (i / 15) * fh * 0.8
        ctx.beginPath()
        ctx.moveTo(sx, sy)
        for (let k = 0; k < 8; k++) {
          const x = sx + (k / 7) * fw * 0.5 + Math.sin(t * 1.5 + i + k) * 6
          const y = sy + Math.cos(t * 1.2 + i + k) * 8 + (k / 7) * (fh * 0.1)
          ctx.lineTo(x, y)
        }
        ctx.stroke()
      }
      ctx.restore()

      // glasses
      ctx.save()
      ctx.globalCompositeOperation = 'screen'
      ctx.strokeStyle = `rgba(0, 229, 255, ${0.35 * intensity})`
      ctx.lineWidth = 1.2
      ctx.beginPath()
      const lw = fw * 0.18
      const lh = fh * 0.13
      const ly = cy - fh * 0.10
      ctx.roundRect(cx - fw * 0.20, ly, lw, lh, 6)
      ctx.roundRect(cx + fw * 0.02, ly, lw, lh, 6)
      ctx.moveTo(cx - fw * 0.02, cy - fh * 0.07)
      ctx.lineTo(cx + fw * 0.02, cy - fh * 0.07)
      ctx.stroke()
      ctx.restore()

      // mouth glow when talking
      if (talking) {
        ctx.save()
        ctx.globalCompositeOperation = 'screen'
        const g = ctx.createRadialGradient(cx, cy + fh * 0.35, 0, cx, cy + fh * 0.35, 18)
        g.addColorStop(0, 'rgba(0, 229, 255, 0.35)')
        g.addColorStop(1, 'rgba(0, 229, 255, 0)')
        ctx.fillStyle = g
        ctx.beginPath()
        ctx.ellipse(cx, cy + fh * 0.35, 14 + Math.sin(t * 8) * 3, 6 + Math.cos(t * 8) * 2, 0, 0, Math.PI * 2)
        ctx.fill()
        ctx.restore()
      }

      // rim light
      ctx.save()
      ctx.globalCompositeOperation = 'screen'
      const rim = ctx.createRadialGradient(cx, cy - fh * 0.05, fw * 0.35, cx, cy - fh * 0.05, fw * 0.55)
      rim.addColorStop(0, 'rgba(0, 229, 255, 0)')
      rim.addColorStop(0.75, `rgba(0, 229, 255, ${0.06 * intensity})`)
      rim.addColorStop(1, 'rgba(0, 229, 255, 0)')
      ctx.fillStyle = rim
      ctx.fillRect(0, 0, w, h)
      ctx.restore()

      raf = requestAnimationFrame(draw)
    }
    draw()
    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('resize', resize)
    }
  }, [talking, listening])

  return (
    <div style={{ width: 340, height: 420, position: 'relative', ...style }}>
      <canvas
        ref={canvasRef}
        style={{
          position: 'absolute',
          inset: 0,
          width: '100%',
          height: '100%',
          zIndex: 2,
          borderRadius: 12,
          opacity: mounted ? 1 : 0,
          transition: 'opacity 600ms ease',
        }}
      />
      <div style={{
        position: 'absolute',
        left: '50%',
        bottom: 8,
        transform: 'translateX(-50%)',
        zIndex: 3,
        display: 'flex',
        alignItems: 'center',
        gap: 8,
        fontFamily: '"Geist Mono", monospace',
        fontSize: 10,
        letterSpacing: '.08em',
        textTransform: 'uppercase',
        color: 'oklch(72% 0.005 240)',
      }}>
        <span style={{
          width: 7, height: 7, borderRadius: 9999,
          background: talking ? '#00E5FF' : listening ? '#42A5F5' : 'oklch(60% 0.14 160)',
          boxShadow: talking ? '0 0 12px #00E5FF' : listening ? '0 0 10px #42A5F5' : 'none',
          animation: talking ? 'om-pulse 0.8s ease-in-out infinite' : 'om-pulse 2.4s ease-in-out infinite',
        }} />
        {talking ? 'speaking' : listening ? 'listening' : 'online - voice ready'}
      </div>
    </div>
  )
}
