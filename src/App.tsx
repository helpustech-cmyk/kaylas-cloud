import { MatrixRain } from './components/MatrixRain'
import { AIAvatar } from './components/AIAvatar'
import { ChatConsole } from './components/ChatConsole'
import { useSpeech } from './hooks/useSpeech'
import './App.css'

function App() {
  const { speak, isSpeaking, mouthLevel } = useSpeech()

  return (
    <div className="shell">
      <MatrixRain />

      <header className="topbar">
        <div className="logo">KAYLAS<span>.CLOUD</span></div>
        <nav className="tabs">
          {['Resume', 'Research', 'Knowledge', 'Repos', 'Training', 'Social'].map((tab) => (
            <button key={tab} className="tab">{tab}</button>
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
          <AIAvatar isSpeaking={isSpeaking} mouthLevel={mouthLevel} />
          <ChatConsole onSpeak={speak} />
        </section>
      </main>
    </div>
  )
}

export default App
