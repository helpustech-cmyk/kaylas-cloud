interface AIAvatarProps {
  isSpeaking: boolean
  mouthLevel: number
}

export function AIAvatar({ isSpeaking, mouthLevel }: AIAvatarProps) {
  const mouthHeight = 4 + mouthLevel * 28

  return (
    <div className={`avatar ${isSpeaking ? 'avatar--speaking' : ''}`}>
      <svg viewBox="0 0 240 240" width="240" height="240">
        <circle cx="120" cy="120" r="110" className="avatar-ring" />
        <circle cx="120" cy="120" r="90" className="avatar-ring avatar-ring--inner" />

        <circle cx="80" cy="100" r="10" className="avatar-eye" />
        <circle cx="160" cy="100" r="10" className="avatar-eye" />

        <rect
          x="90"
          y={150 - mouthHeight / 2}
          width="60"
          height={mouthHeight}
          rx="8"
          className="avatar-mouth"
        />
      </svg>
      <div className="avatar-status">
        {isSpeaking ? 'TRANSMITTING…' : 'STANDBY'}
      </div>
    </div>
  )
}
