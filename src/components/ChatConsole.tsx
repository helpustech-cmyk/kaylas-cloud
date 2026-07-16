import { useState, type FormEvent } from 'react'
import { answer } from '../lib/retrieval'
import { resolveNavIntent, type TabId } from '../lib/navigation'

interface LogLine {
  id: number
  role: 'user' | 'ai'
  text: string
}

interface ChatConsoleProps {
  onSpeak: (text: string) => void
  onNavigate?: (tabId: TabId) => void
}

export function ChatConsole({ onSpeak, onNavigate }: ChatConsoleProps) {
  const [input, setInput] = useState('')
  const [log, setLog] = useState<LogLine[]>([
    {
      id: 0,
      role: 'ai',
      text: "Hi, I'm Kailas's AI twin. Ask me about my role, AI expertise, or how to connect — or say 'open resume' to navigate.",
    },
  ])

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    const text = input.trim()
    if (!text) return

    const navTab = resolveNavIntent(text)
    const reply = navTab ? `Opening ${navTab} for you.` : answer(text)

    setLog((prev) => [
      ...prev,
      { id: prev.length, role: 'user', text },
      { id: prev.length + 1, role: 'ai', text: reply },
    ])
    onSpeak(reply)
    if (navTab && onNavigate) onNavigate(navTab)
    setInput('')
  }

  return (
    <div className="chat-console">
      <div className="chat-log">
        {log.map((line) => (
          <p key={line.id} className={`chat-line chat-line--${line.role}`}>
            <span className="chat-prefix">{line.role === 'ai' ? '>>' : '$'}</span> {line.text}
          </p>
        ))}
      </div>
      <form className="chat-form" onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask Kailas's AI twin..."
          autoComplete="off"
        />
        <button type="submit">Send</button>
      </form>
    </div>
  )
}
