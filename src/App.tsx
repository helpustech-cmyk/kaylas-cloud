import { useState } from 'react'
import { MatrixRain } from './components/MatrixRain'
import { FloatingAvatarWidget } from './components/FloatingAvatarWidget'
import { ResumeTab } from './components/tabs/ResumeTab'
import { PlaceholderTab } from './components/tabs/PlaceholderTab'
import './App.css'

const TABS = [
  { id: 'resume', label: 'Resume' },
  { id: 'research', label: 'Research' },
  { id: 'knowledge', label: 'Knowledge' },
  { id: 'repos', label: 'Repos' },
  { id: 'training', label: 'Training' },
  { id: 'social', label: 'Social' },
] as const

type TabId = (typeof TABS)[number]['id']

const PLACEHOLDER_COPY: Record<Exclude<TabId, 'resume'>, { title: string; description: string }> = {
  research: {
    title: 'Research Lab & YouTube',
    description: 'Research papers and video breakdowns on AI-driven customer experience — coming soon.',
  },
  knowledge: {
    title: 'AI Knowledge Hub',
    description: 'A growing library of approved research and writing on Service + AI — coming soon.',
  },
  repos: {
    title: 'Automation Repos',
    description: 'Links to automation projects and tools on GitHub/Hugging Face — coming soon.',
  },
  training: {
    title: 'Service Leaders Training',
    description: 'Training videos and frameworks for frontline and service leadership — coming soon.',
  },
  social: {
    title: 'Social Media Wall',
    description: 'A unified feed of LinkedIn, X, and Telegram posts — coming soon.',
  },
}

function App() {
  const [activeTab, setActiveTab] = useState<TabId>('resume')

  return (
    <div className="shell">
      <MatrixRain />

      <header className="topbar">
        <div className="logo">KAYLAS<span>.CLOUD</span></div>
        <nav className="tabs">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              className={`tab ${activeTab === tab.id ? 'tab--active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </header>

      <main className="layout">
        <aside className="side-panel">
          <div className="contact-blur">
            <p>📞 +91 ●●●●● ●●●●●</p>
            <p>✉️ ●●●●●●●@●●●●.com</p>
          </div>
          <button className="cta">Book a Call</button>
          <button className="cta cta--ghost">Chat Now</button>
        </aside>

        <section className="stage">
          {activeTab === 'resume' ? (
            <ResumeTab />
          ) : (
            <PlaceholderTab {...PLACEHOLDER_COPY[activeTab]} />
          )}
        </section>
      </main>

      <FloatingAvatarWidget />
    </div>
  )
}

export default App
