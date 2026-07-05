import { useState } from 'react'
import { AIAvatar } from './AIAvatar'
import { ChatConsole } from './ChatConsole'
import { useSpeech } from '../hooks/useSpeech'

export function FloatingAvatarWidget() {
  const [open, setOpen] = useState(false)
  const { speak, isSpeaking, mouthLevel } = useSpeech()

  return (
    <div className={`avatar-widget ${open ? 'avatar-widget--open' : ''}`}>
      {open && (
        <div className="avatar-widget-panel">
          <AIAvatar isSpeaking={isSpeaking} mouthLevel={mouthLevel} />
          <ChatConsole onSpeak={speak} />
        </div>
      )}
      <button className="avatar-widget-toggle" onClick={() => setOpen((v) => !v)}>
        {open ? 'Close' : 'Chat with AI Twin'}
      </button>
    </div>
  )
}
