import { useState, useRef, useEffect, useCallback } from 'react'
import { MatrixRain } from './components/MatrixRain'
import { BootSeq } from './components/BootSeq'
import { AboutTab } from './components/tabs/AboutTab'
import { ResumeTab } from './components/tabs/ResumeTab'
import { NewsTab } from './components/tabs/NewsTab'
import { ResearchTab } from './components/tabs/ResearchTab'
import { ReposTab } from './components/tabs/ReposTab'
import { TrainingTab } from './components/tabs/TrainingTab'
import { SocialTab } from './components/tabs/SocialTab'
import { TowerTab } from './components/tabs/TowerTab'
import { profile } from './data/resume'
import type { TabId } from './lib/navigation'
import './App.css'

const TABS: { id: TabId; label: string }[] = [
  { id: 'about', label: '01 About' },
  { id: 'resume', label: '02 Resume' },
  { id: 'news', label: '03 AI News' },
  { id: 'research', label: '04 Research' },
  { id: 'repos', label: '05 Repos' },
  { id: 'training', label: '06 Training' },
  { id: 'social', label: '07 Social' },
  { id: 'tower', label: '08 Tower' },
]

const API_BASE = '/api/v1'

const COUNTRY_CODES = [
  '+91', '+1', '+44', '+61', '+86', '+49', '+33', '+81', '+7', '+55',
  '+82', '+39', '+34', '+31', '+46', '+41', '+47', '+45', '+358', '+30',
  '+48', '+351', '+43', '+32', '+36', '+420', '+353', '+40', '+359', '+385',
  '+381', '+386', '+421', '+386', '+372', '+371', '+370', '+352', '+356', '+377',
  '+389', '+373', '+382', '+387', '+90', '+972', '+966', '+971', '+974', '+968',
  '+20', '+212', '+213', '+216', '+218', '+221', '+222', '+223', '+224', '+225',
  '+226', '+227', '+228', '+229', '+230', '+231', '+232', '+233', '+234', '+235',
  '+236', '+237', '+238', '+239', '+240', '+241', '+242', '+243', '+244', '+245',
  '+246', '+247', '+248', '+249', '+250', '+251', '+252', '+253', '+254', '+255',
  '+256', '+257', '+258', '+260', '+261', '+262', '+263', '+264', '+265', '+266',
  '+267', '+268', '+269', '+27', '+92', '+93', '+94', '+95', '+98', '+63',
  '+62', '+60', '+66', '+84', '+880', '+856', '+855', '+975', '+977', '+670',
  '+673', '+674', '+675', '+676', '+677', '+678', '+679', '+680', '+681', '+682',
  '+683', '+685', '+686', '+687', '+688', '+689', '+690', '+691', '+692',
]

function App() {
  const [tab, setTab] = useState<TabId>('about')
  const [booting, setBooting] = useState(true)
  const [talking, setTalking] = useState(false)
  const [voiceOn, setVoiceOn] = useState(true)
  const [listening, setListening] = useState(false)
  const [contactUnlocked, setContactUnlocked] = useState(false)
  const [leadOpen, setLeadOpen] = useState(false)
  const [leadLoading, setLeadLoading] = useState(false)
  const [leadError, setLeadError] = useState('')
  const [leadSuccess, setLeadSuccess] = useState(false)
  const [stats, setStats] = useState<{uptime_days: number; published_posts: number; total_leads: number; last_publish: string | null; services_running: number} | null>(null)
  const [messages, setMessages] = useState<{ who: string; text: string }[]>([
    { who: 'twin', text: "I'm Kailas's digital twin. Ask me about his work, his vision for Service + AI, or say 'open resume' to navigate. I can also speak — try the mic button." },
  ])
  const [chatLoading, setChatLoading] = useState(false)
  const chatLogRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const recRef = useRef<any>(null)
  const nameRef = useRef<HTMLInputElement>(null)
  const emailRef = useRef<HTMLInputElement>(null)
  const companyRef = useRef<HTMLInputElement>(null)
  const phoneRef = useRef<HTMLInputElement>(null)
  const countryRef = useRef<HTMLSelectElement>(null)
  const sessionId = useRef('session_' + Math.random().toString(36).slice(2, 10) + '_' + Date.now().toString(36))

  useEffect(() => {
    const t = setTimeout(() => setBooting(false), 5200)
    return () => clearTimeout(t)
  }, [])

  useEffect(() => {
    fetch(API_BASE + '/stats')
      .then(r => r.json())
      .then(setStats)
      .catch(() => {})
  }, [])

  const speak = useCallback((text: string) => {
    if (!voiceOn || !('speechSynthesis' in window)) return
    try {
      speechSynthesis.cancel()
      const u = new SpeechSynthesisUtterance(text)
      u.rate = 0.95; u.pitch = 0.85
      const vs = speechSynthesis.getVoices()
      u.voice = vs.find((v: any) => /en[-_](IN|GB)/i.test(v.lang) && /male|daniel|rishi/i.test(v.name)) || vs.find((v: any) => /en[-_]IN/i.test(v.lang)) || vs.find((v: any) => /en/i.test(v.lang)) || null
      u.onstart = () => setTalking(true)
      u.onend = () => setTalking(false)
      speechSynthesis.speak(u)
    } catch (e) {}
  }, [voiceOn])

  const answer = useCallback(async (q: string) => {
    setMessages(prev => [...prev, { who: 'you', text: q }])
    setChatLoading(true)
    try {
      const res = await fetch(`${API_BASE}/twin/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId.current,
          messages: [
            ...messages.filter(m => m.who !== 'system').map(m => ({
              role: m.who === 'you' ? 'user' : 'assistant',
              content: m.text,
            })),
            { role: 'user', content: q },
          ],
        }),
      })
      if (!res.ok) throw new Error('API error')
      const data = await res.json()
      const reply = data.content || "I'm processing your question. Give me a moment."
      setMessages(prev => [...prev, { who: 'twin', text: reply }])
      speak(reply)
    } catch (e) {
      const fallback = "I'm having trouble reaching my knowledge base right now. Please try again in a moment."
      setMessages(prev => [...prev, { who: 'twin', text: fallback }])
      speak(fallback)
    } finally {
      setChatLoading(false)
    }
  }, [messages, speak])

  const handleLeadSubmit = useCallback(async () => {
    const name = nameRef.current?.value.trim()
    const email = emailRef.current?.value.trim()
    const phone = phoneRef.current?.value.trim()
    const country_code = countryRef.current?.value || '+91'
    const company = companyRef.current?.value.trim()
    if (!name || !email) {
      setLeadError('Name and email are required')
      return
    }
    setLeadLoading(true)
    setLeadError('')
    try {
      const res = await fetch(`${API_BASE}/leads`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, phone: phone || undefined, country_code, company: company || undefined, source: 'website' }),
      })
      if (!res.ok) throw new Error('Failed to submit')
      setLeadSuccess(true)
      setContactUnlocked(true)
      setMessages(prev => [...prev, { who: 'twin', text: "Thanks — Kailas just got your details on Telegram. His contact card is unlocked." }])
    } catch (e) {
      setLeadError('Something went wrong. Please try again or email directly.')
    } finally {
      setLeadLoading(false)
    }
  }, [])

  const micClick = useCallback(() => {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    if (!SR) {
      setMessages(prev => [...prev, { who: 'twin', text: 'Voice input needs Chrome or Edge — the text box always works.' }])
      return
    }
    if (listening) { try { recRef.current?.stop() } catch (e) {} return }
    const rec = new SR()
    recRef.current = rec
    rec.lang = 'en-IN'; rec.interimResults = false
    rec.onresult = (e: any) => { const t = e.results[0][0].transcript; answer(t) }
    rec.onend = () => setListening(false)
    rec.onerror = () => setListening(false)
    setListening(true)
    try { rec.start() } catch (e) { setListening(false) }
  }, [listening, answer])

  useEffect(() => { chatLogRef.current?.scrollTo({ top: chatLogRef.current.scrollHeight }) }, [messages])

  const go = (id: TabId) => () => setTab(id)
  const twinStatus = chatLoading ? 'thinking...' : (listening ? 'listening...' : (talking ? 'speaking' : 'online - voice ready'))

  return (
    <div data-theme="dark" style={{ background: 'oklch(14% 0.005 240)', color: 'oklch(96% 0.005 240)', fontFamily: '"Geist", system-ui, sans-serif', minHeight: '100vh', display: 'flex', flexDirection: 'column', position: 'relative' }}>
      <MatrixRain />
      {booting && (
        <div style={{ position: 'fixed', inset: 0, background: 'oklch(10% 0.005 240)', zIndex: 1500, display: 'flex', flexDirection: 'column', padding: 48, cursor: 'pointer' }} onClick={() => setBooting(false)}>
          <BootSeq lines="$ ssh visitor@kaylas.cloud|-> connected - digital twin runtime v2.4.1|-> loading profile: KAILAS_SWAMI ............ ok|-> mounting skills: [lifecycle] [omnichannel] [marketing-cloud] [telephony] [ai-cx] [revenue-eng]|-> knowledge base: resume + blogs + ai-news + research papers - voice: ready|-> twin.online = true | model: brand-expert-v1 | latency: 12ms" />
          <div style={{ marginTop: 'auto', fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(55% 0.005 240)' }}>click anywhere to skip</div>
        </div>
      )}
      <div style={{ height: 44, display: 'flex', alignItems: 'center', gap: 12, padding: '0 16px', borderBottom: '1px solid oklch(26% 0.005 240)', flex: 'none', position: 'sticky', top: 0, background: 'oklch(14% 0.005 240)', zIndex: 100 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flex: 'none' }}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="oklch(72% 0.18 215)" strokeWidth="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
          <span style={{ fontWeight: 600, letterSpacing: '-0.02em', fontSize: 14 }}>kaylas.cloud</span>
        </div>
        <div style={{ display: 'flex', gap: 2, marginLeft: 16, fontSize: 12, overflowX: 'auto' }}>
          {TABS.map(t => (
            <button key={t.id} onClick={go(t.id)}
              style={{ padding: '6px 10px', border: 0, cursor: 'pointer', font: 'inherit', fontSize: 12, whiteSpace: 'nowrap', background: tab === t.id ? 'oklch(22% 0.06 215)' : 'transparent', color: tab === t.id ? 'oklch(72% 0.18 215)' : 'oklch(72% 0.005 240)', transition: 'background 120ms, color 120ms' }}
            >{t.label}</button>
          ))}
        </div>
        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 12, fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(72% 0.005 240)', flex: 'none' }}>
          <span><span style={{ display: 'inline-block', width: 7, height: 7, borderRadius: 9999, background: 'oklch(60% 0.14 160)', animation: 'om-pulse 2.4s ease-in-out infinite' }}></span>vps live</span>
          <span>3 automations - n8n ok</span>
        </div>
      </div>
      <div style={{ flex: 1, display: 'flex', minHeight: 0, alignItems: 'stretch' }}>
        <div style={{ width: 232, flex: 'none', borderRight: '1px solid oklch(26% 0.005 240)', padding: '20px 16px', display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div>
            <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(55% 0.005 240)', marginBottom: 8 }}>Contact</div>
            {contactUnlocked ? (
              <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 12, lineHeight: '20px', color: 'oklch(96% 0.005 240)' }}>
                <div>{profile.phone}</div>
                <div>{profile.email}</div>
                <div style={{ color: 'oklch(72% 0.005 240)' }}>{profile.location}</div>
              </div>
            ) : (
              <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 12, lineHeight: '20px', color: 'oklch(72% 0.005 240)' }}>
                <div style={{ filter: 'blur(5px)', userSelect: 'none' }}>+91 93.. .... 56</div>
                <div style={{ filter: 'blur(5px)', userSelect: 'none' }}>kailashjd@out.....com</div>
                <div>Navi Mumbai, IN</div>
              </div>
            )}
            {!contactUnlocked && <div style={{ fontSize: 11, color: 'oklch(55% 0.005 240)', marginTop: 6 }}>Unlocks after you introduce yourself</div>}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <button style={{ background: 'oklch(72% 0.18 215)', color: 'oklch(8% 0 0)', fontWeight: 500, fontSize: 13, textAlign: 'center', padding: 10, border: 0, cursor: 'pointer', fontFamily: 'inherit' }}>Book a call</button>
            <button onClick={() => inputRef.current?.focus()}
              style={{ border: '1px solid oklch(34% 0.005 240)', background: 'transparent', fontSize: 13, textAlign: 'center', padding: 10, color: 'oklch(96% 0.005 240)', cursor: 'pointer', fontFamily: 'inherit' }}>Chat with my twin</button>
            <button onClick={() => setLeadOpen(true)}
              style={{ border: '1px solid oklch(34% 0.005 240)', background: 'transparent', fontSize: 13, textAlign: 'center', padding: 10, color: 'oklch(96% 0.005 240)', cursor: 'pointer', fontFamily: 'inherit' }}>View contact details</button>
          </div>
          <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: 12 }}>
            <div style={{ border: '1px solid oklch(26% 0.005 240)', padding: 12 }}>
              <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 10, textTransform: 'uppercase', letterSpacing: '.08em', color: 'oklch(55% 0.005 240)', marginBottom: 8 }}>Live from the VPS</div>
              <div style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, lineHeight: '18px', color: 'oklch(72% 0.005 240)' }}>
                <div>uptime <span style={{ color: 'oklch(60% 0.14 160)' }}>{stats ? stats.uptime_days + 'd' : '...'}</span></div>
                <div>posts published <span style={{ color: 'oklch(72% 0.18 215)' }}>{stats ? stats.published_posts : '...'}</span></div>
                <div>leads captured <span style={{ color: 'oklch(72% 0.18 215)' }}>{stats ? stats.total_leads : '...'}</span></div>
              </div>
            </div>
            <div style={{ border: '1px solid oklch(26% 0.005 240)', padding: '10px 12px', fontFamily: '"Geist Mono", monospace', fontSize: 10, lineHeight: '16px', color: 'oklch(55% 0.005 240)' }}>Runs on Hostinger VPS -&gt;<br /><span style={{ color: 'oklch(72% 0.005 240)' }}>affiliate - same stack I teach</span></div>
          </div>
        </div>
        <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column' }}>
          {tab === 'about' && <AboutTab onNavigate={setTab} talking={talking} listening={listening} />}
          {tab === 'resume' && <ResumeTab />}
          {tab === 'news' && <NewsTab />}
          {tab === 'research' && <ResearchTab />}
          {tab === 'repos' && <ReposTab />}
          {tab === 'training' && <TrainingTab />}
          {tab === 'social' && <SocialTab />}
          {tab === 'tower' && <TowerTab />}
        </div>
      </div>
      <div style={{ position: 'fixed', right: 16, bottom: 16, width: 360, zIndex: 1100, border: '1px solid oklch(34% 0.005 240)', background: 'oklch(14% 0.005 240)', boxShadow: '0 0 0 1px oklch(26% 0.005 240), 0 8px 24px -8px oklch(0% 0 0 / 0.5)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '10px 12px', borderBottom: '1px solid oklch(26% 0.005 240)' }}>
          <span style={{ width: 8, height: 8, borderRadius: 9999, background: chatLoading ? 'oklch(72% 0.18 215)' : 'oklch(60% 0.14 160)', animation: chatLoading ? 'none' : 'om-pulse 2.4s ease-in-out infinite' }}></span>
          <span style={{ fontFamily: '"Geist Mono", monospace', fontSize: 11, color: 'oklch(72% 0.005 240)' }}>kailas.twin - {twinStatus}</span>
          <button onClick={() => setVoiceOn(!voiceOn)}
            style={{ marginLeft: 'auto', border: '1px solid oklch(34% 0.005 240)', background: 'transparent', color: 'oklch(72% 0.005 240)', fontFamily: '"Geist Mono", monospace', fontSize: 10, padding: '4px 8px', cursor: 'pointer' }}
          >{voiceOn ? 'voice on' : 'muted'}</button>
        </div>
        <div ref={chatLogRef} style={{ height: 180, overflowY: 'auto', padding: 12, display: 'flex', flexDirection: 'column', gap: 8 }}>
          {messages.map((m, i) => (
            <div key={i} style={m.who === 'you'
              ? { alignSelf: 'flex-end', maxWidth: '85%', background: 'oklch(22% 0.06 215)', color: 'oklch(96% 0.005 240)', padding: '8px 10px', fontSize: 12, lineHeight: '18px' }
              : { alignSelf: 'flex-start', maxWidth: '85%', border: '1px solid oklch(26% 0.005 240)', color: 'oklch(72% 0.005 240)', padding: '8px 10px', fontSize: 12, lineHeight: '18px', fontFamily: '"Geist Mono", monospace' }
            }>{m.text}</div>
          ))}
          {chatLoading && (
            <div style={{ alignSelf: 'flex-start', maxWidth: '85%', border: '1px solid oklch(26% 0.005 240)', color: 'oklch(55% 0.005 240)', padding: '8px 10px', fontSize: 12, lineHeight: '18px', fontFamily: '"Geist Mono", monospace' }}>
              thinking<span style={{ animation: 'om-pulse 1.5s ease-in-out infinite' }}>...</span>
            </div>
          )}
        </div>
        <div style={{ display: 'flex', borderTop: '1px solid oklch(26% 0.005 240)' }}>
          <span style={{ fontFamily: '"Geist Mono", monospace', fontSize: 12, color: 'oklch(72% 0.18 215)', padding: '12px 0 12px 12px' }}>&gt;</span>
          <input ref={inputRef} onKeyDown={e => { if (e.key === 'Enter' && (e.target as HTMLInputElement).value.trim() && !chatLoading) { const v = (e.target as HTMLInputElement).value.trim(); (e.target as HTMLInputElement).value = ''; answer(v) } }}
            placeholder="Ask Kailas's twin about his work..."
            style={{ flex: 1, background: 'transparent', border: 0, outline: 'none', color: 'oklch(96% 0.005 240)', fontSize: 13, padding: 12, fontFamily: 'inherit' }} />
          <button onClick={micClick}
            style={{ border: 0, borderLeft: '1px solid oklch(26% 0.005 240)', background: 'transparent', color: 'oklch(72% 0.18 215)', fontFamily: '"Geist Mono", monospace', fontSize: 11, padding: '0 12px', cursor: 'pointer' }}
          >{listening ? 'rec' : 'mic'}</button>
        </div>
      </div>
      {leadOpen && (
        <div style={{ position: 'fixed', inset: 0, background: 'oklch(0% 0 0 / 0.45)', zIndex: 1200, display: 'grid', placeItems: 'center' }} onClick={() => setLeadOpen(false)}>
          <div style={{ width: 400, background: 'oklch(18% 0.005 240)', border: '1px solid oklch(34% 0.005 240)', boxShadow: '0 24px 64px -16px oklch(0% 0 0 / 0.5)', padding: 24 }} onClick={e => e.stopPropagation()}>
            <div style={{ fontSize: 16, fontWeight: 600 }}>Introduce yourself</div>
            <div style={{ fontSize: 13, lineHeight: '20px', color: 'oklch(72% 0.005 240)', marginTop: 6 }}>Your details go straight to Kailas on Telegram. Contact card unlocks immediately.</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 16 }}>
              <input ref={nameRef} placeholder="Name" style={{ background: 'oklch(14% 0.005 240)', border: '1px solid oklch(34% 0.005 240)', color: 'oklch(96% 0.005 240)', fontSize: 13, padding: '10px 12px', outline: 'none', fontFamily: 'inherit' }} />
              <input ref={emailRef} placeholder="Work email" style={{ background: 'oklch(14% 0.005 240)', border: '1px solid oklch(34% 0.005 240)', color: 'oklch(96% 0.005 240)', fontSize: 13, padding: '10px 12px', outline: 'none', fontFamily: 'inherit' }} />
              <div style={{ display: 'flex', gap: 8 }}>
                <select ref={countryRef} defaultValue="+91" style={{ width: 80, background: 'oklch(14% 0.005 240)', border: '1px solid oklch(34% 0.005 240)', color: 'oklch(96% 0.005 240)', fontSize: 13, padding: '10px 4px', outline: 'none', fontFamily: 'inherit' }}>
                  {COUNTRY_CODES.map(cc => <option key={cc} value={cc}>{cc}</option>)}
                </select>
                <input ref={phoneRef} placeholder="Phone (optional)" type="tel" style={{ flex: 1, background: 'oklch(14% 0.005 240)', border: '1px solid oklch(34% 0.005 240)', color: 'oklch(96% 0.005 240)', fontSize: 13, padding: '10px 12px', outline: 'none', fontFamily: 'inherit' }} />
              </div>
              <input ref={companyRef} placeholder="Company (optional)" style={{ background: 'oklch(14% 0.005 240)', border: '1px solid oklch(34% 0.005 240)', color: 'oklch(96% 0.005 240)', fontSize: 13, padding: '10px 12px', outline: 'none', fontFamily: 'inherit' }} />
            </div>
            {leadError && <div style={{ fontSize: 12, color: 'oklch(60% 0.18 20)', marginTop: 8 }}>{leadError}</div>}
            {leadSuccess ? (
              <div style={{ fontSize: 13, color: 'oklch(60% 0.14 160)', marginTop: 16 }}>✓ Details sent! Contact card unlocked.</div>
            ) : (
              <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
                <button onClick={handleLeadSubmit} disabled={leadLoading}
                  style={{ flex: 1, background: leadLoading ? 'oklch(55% 0.005 240)' : 'oklch(72% 0.18 215)', color: 'oklch(8% 0 0)', fontWeight: 500, fontSize: 13, padding: 10, border: 0, cursor: leadLoading ? 'default' : 'pointer', fontFamily: 'inherit' }}
                >{leadLoading ? 'Sending...' : 'Unlock contact details'}</button>
                <button onClick={() => setLeadOpen(false)}
                  style={{ border: '1px solid oklch(34% 0.005 240)', background: 'transparent', color: 'oklch(96% 0.005 240)', fontSize: 13, padding: '10px 16px', cursor: 'pointer', fontFamily: 'inherit' }}
                >Cancel</button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default App
