import { useState, type FormEvent } from 'react'
import { answer } from '../lib/retrieval'

interface LogLine {
  id: number
  role: 'user' | 'ai'
  text: string
}

interface ChatConsoleProps {
  onSpeak: (text: string) => void
}

export function ChatConsole({ onSpeak }: ChatConsoleProps) {
  const [input, setInput] = useState('')
  const [log, setLog] = useState<LogLine[]>([
    {
      id: 0,
      role: 'ai',
      text: "Hi, I'm Kailas's AI twin. Ask me about my role, AI expertise, or how to connect.",
    },
  ])

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    const text = input.trim()
    if (!text) return

    const reply = answer(text)
    setLog((prev) => [
      ...prev,
      { id: prev.length, role: 'user', text },
      { id: prev.length + 1, role: 'ai', text: reply },
    ])
    onSpeak(reply)
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
